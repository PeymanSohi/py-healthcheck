"""
Command-line interface for py-healthcheck.
"""

import asyncio
import json
import sys
from typing import Dict, List, Optional

import click

from .core import run_health_checks_sync
from .checks import (
    check_postgres,
    check_mysql,
    check_redis,
    check_mongodb,
    check_elasticsearch,
    check_http,
)


# Built-in check types and their functions
CHECK_TYPES = {
    "postgres": check_postgres,
    "mysql": check_mysql,
    "redis": check_redis,
    "mongodb": check_mongodb,
    "elasticsearch": check_elasticsearch,
    "http": check_http,
}


def parse_check_spec(spec: str) -> Dict[str, str]:
    """Parse a check specification string.
    
    Args:
        spec: Check specification in format "TYPE:URL" or "TYPE:host:port"
        
    Returns:
        Dictionary with parsed check information
    """
    parts = spec.split(":", 1)
    if len(parts) != 2:
        raise click.BadParameter(f"Invalid check specification: {spec}. Expected format: TYPE:URL")
    
    check_type, url_or_config = parts
    
    if check_type not in CHECK_TYPES:
        available_types = ", ".join(CHECK_TYPES.keys())
        raise click.BadParameter(f"Unknown check type: {check_type}. Available types: {available_types}")
    
    return {
        "type": check_type,
        "config": url_or_config
    }


def create_check_function(check_type: str, config: str):
    """Create a check function for the given type and configuration.
    
    Args:
        check_type: Type of check to create
        config: Configuration string (URL or host:port)
        
    Returns:
        Function that performs the health check
    """
    check_func = CHECK_TYPES[check_type]
    
    def wrapper():
        if check_type in ["postgres", "mysql", "mongodb", "elasticsearch"]:
            # For databases, treat config as connection string
            check_func(connection_string=config)
        elif check_type == "redis":
            # For Redis, treat config as connection string
            check_func(connection_string=config)
        elif check_type == "http":
            # For HTTP, treat config as URL
            check_func(url=config)
        else:
            # Fallback: try as connection string
            check_func(connection_string=config)
    
    return wrapper


def format_output_json(result: Dict, verbose: bool = False) -> str:
    """Format health check result as JSON.
    
    Args:
        result: Health check result dictionary
        verbose: Whether to include verbose information
        
    Returns:
        Formatted JSON string
    """
    if not verbose:
        # Remove detailed timing information for non-verbose output
        output = {
            "status": result["status"],
            "checks": result["checks"]
        }
        if "details" in result and result["details"]:
            output["details"] = result["details"]
    else:
        output = result
    
    return json.dumps(output, indent=2)


def format_output_table(result: Dict) -> str:
    """Format health check result as a table.
    
    Args:
        result: Health check result dictionary
        
    Returns:
        Formatted table string
    """
    try:
        from rich.console import Console
        from rich.table import Table
        from rich import box
        
        console = Console()
        table = Table(title="Health Check Results", box=box.ROUNDED)
        
        table.add_column("Check", style="cyan", no_wrap=True)
        table.add_column("Status", justify="center")
        table.add_column("Details", style="dim")
        
        for check_name, status in result["checks"].items():
            status_style = "green" if status == "ok" else "red"
            details = result.get("details", {}).get(check_name, "")
            
            table.add_row(
                check_name,
                f"[{status_style}]{status}[/{status_style}]",
                details
            )
        
        # Add summary row
        summary = result.get("summary", {})
        table.add_row(
            "SUMMARY",
            f"[{'green' if result['status'] == 'ok' else 'red'}]{result['status'].upper()}[/{'green' if result['status'] == 'ok' else 'red'}]",
            f"Total: {summary.get('total', 0)}, Passed: {summary.get('passed', 0)}, Failed: {summary.get('failed', 0)}"
        )
        
        output = console.capture()
        console.print(table)
        return output.get()
        
    except ImportError:
        # Fallback to simple text format if rich is not available
        lines = ["Health Check Results", "=" * 50]
        
        for check_name, status in result["checks"].items():
            details = result.get("details", {}).get(check_name, "")
            status_symbol = "✓" if status == "ok" else "✗"
            lines.append(f"{status_symbol} {check_name}: {status}")
            if details:
                lines.append(f"  Details: {details}")
        
        summary = result.get("summary", {})
        lines.append(f"\nSummary: {result['status'].upper()}")
        lines.append(f"Total: {summary.get('total', 0)}, Passed: {summary.get('passed', 0)}, Failed: {summary.get('failed', 0)}")
        
        return "\n".join(lines)


@click.command()
@click.option(
    "--check",
    "checks",
    multiple=True,
    help="Check specification in format TYPE:URL (e.g., postgres:postgresql://user:pass@host/db)"
)
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json", "table"], case_sensitive=False),
    default="json",
    help="Output format"
)
@click.option(
    "--timeout",
    type=float,
    default=5.0,
    help="Timeout in seconds for each check"
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Include verbose information in output"
)
@click.option(
    "--quiet",
    "-q",
    is_flag=True,
    help="Only output the final status (ok/fail)"
)
def main(
    checks: List[str],
    output_format: str,
    timeout: float,
    verbose: bool,
    quiet: bool
):
    """py-healthcheck - A comprehensive health check tool for Python applications.
    
    Examples:
    
    \b
    # Check a PostgreSQL database
    py-healthcheck --check postgres:postgresql://user:pass@localhost/mydb
    
    \b
    # Check multiple services
    py-healthcheck --check postgres:postgresql://user:pass@localhost/mydb \\
                   --check redis:redis://localhost:6379 \\
                   --check http:http://localhost:8080/health
    
    \b
    # Use table format with verbose output
    py-healthcheck --check postgres:postgresql://user:pass@localhost/mydb \\
                   --format table --verbose
    """
    if not checks:
        click.echo("Error: At least one --check option is required", err=True)
        click.echo("Use --help for usage information", err=True)
        sys.exit(1)
    
    # Parse and register checks
    from .core import register_health_check
    
    for check_spec in checks:
        try:
            parsed = parse_check_spec(check_spec)
            check_func = create_check_function(parsed["type"], parsed["config"])
            register_health_check(f"{parsed['type']}_{len(checks)}", check_func)
        except Exception as e:
            click.echo(f"Error parsing check '{check_spec}': {str(e)}", err=True)
            sys.exit(1)
    
    # Run health checks
    try:
        result = run_health_checks_sync(timeout=timeout, include_details=True)
        
        # Format output
        if quiet:
            output = result["status"]
        elif output_format.lower() == "json":
            output = format_output_json(result, verbose)
        else:  # table format
            output = format_output_table(result)
        
        click.echo(output)
        
        # Exit with appropriate code
        sys.exit(0 if result["status"] == "ok" else 1)
        
    except Exception as e:
        click.echo(f"Error running health checks: {str(e)}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
