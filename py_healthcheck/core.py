"""
Core health check functionality for py-healthcheck.

This module provides the main health check registry and execution engine,
supporting both synchronous and asynchronous health checks.
"""

import asyncio
import inspect
import time
from typing import Any, Awaitable, Callable, Dict, List, Optional, Union

from .exceptions import HealthCheckError


class HealthCheckRegistry:
    """Registry for health check functions."""
    
    def __init__(self):
        self._checks: Dict[str, Callable] = {}
        self._async_checks: Dict[str, Callable] = {}
    
    def register(self, name: str, func: Callable) -> None:
        """Register a health check function.
        
        Args:
            name: Unique name for the health check
            func: Function to execute for the health check
        """
        if inspect.iscoroutinefunction(func):
            self._async_checks[name] = func
        else:
            self._checks[name] = func
    
    def unregister(self, name: str) -> None:
        """Unregister a health check function.
        
        Args:
            name: Name of the health check to remove
        """
        self._checks.pop(name, None)
        self._async_checks.pop(name, None)
    
    def get_checks(self) -> Dict[str, Callable]:
        """Get all registered synchronous checks."""
        return self._checks.copy()
    
    def get_async_checks(self) -> Dict[str, Callable]:
        """Get all registered asynchronous checks."""
        return self._async_checks.copy()
    
    def clear(self) -> None:
        """Clear all registered checks."""
        self._checks.clear()
        self._async_checks.clear()


# Global registry instance
_registry = HealthCheckRegistry()


def healthcheck(name: str) -> Callable:
    """Decorator to register a health check function.
    
    Args:
        name: Unique name for the health check
        
    Returns:
        Decorated function
        
    Example:
        @healthcheck("database")
        async def check_database():
            # Check database connection
            pass
    """
    def decorator(func: Callable) -> Callable:
        _registry.register(name, func)
        return func
    return decorator


def register_health_check(name: str, func: Callable) -> None:
    """Register a health check function programmatically.
    
    Args:
        name: Unique name for the health check
        func: Function to execute for the health check
    """
    _registry.register(name, func)


def unregister_health_check(name: str) -> None:
    """Unregister a health check function.
    
    Args:
        name: Name of the health check to remove
    """
    _registry.unregister(name)


async def _run_single_check(name: str, func: Callable, timeout: float = 5.0) -> Dict[str, Any]:
    """Run a single health check with timeout.
    
    Args:
        name: Name of the health check
        func: Function to execute
        timeout: Timeout in seconds
        
    Returns:
        Dictionary with check result
    """
    start_time = time.time()
    
    try:
        if inspect.iscoroutinefunction(func):
            result = await asyncio.wait_for(func(), timeout=timeout)
        else:
            # Run sync function in thread pool
            loop = asyncio.get_event_loop()
            result = await asyncio.wait_for(
                loop.run_in_executor(None, func), 
                timeout=timeout
            )
        
        duration = time.time() - start_time
        return {
            "name": name,
            "status": "ok",
            "duration": duration,
            "message": None
        }
    except asyncio.TimeoutError:
        duration = time.time() - start_time
        return {
            "name": name,
            "status": "fail",
            "duration": duration,
            "message": f"Check timed out after {timeout} seconds"
        }
    except HealthCheckError as e:
        duration = time.time() - start_time
        return {
            "name": name,
            "status": "fail",
            "duration": duration,
            "message": str(e)
        }
    except Exception as e:
        duration = time.time() - start_time
        return {
            "name": name,
            "status": "fail",
            "duration": duration,
            "message": f"Unexpected error: {str(e)}"
        }


async def run_health_checks(
    checks: Optional[List[str]] = None,
    timeout: float = 5.0,
    include_details: bool = True
) -> Dict[str, Any]:
    """Run all registered health checks.
    
    Args:
        checks: Optional list of specific check names to run
        timeout: Timeout in seconds for each check
        include_details: Whether to include detailed error messages
        
    Returns:
        Dictionary with overall status and individual check results
    """
    sync_checks = _registry.get_checks()
    async_checks = _registry.get_async_checks()
    
    # Filter checks if specific ones requested
    if checks:
        sync_checks = {k: v for k, v in sync_checks.items() if k in checks}
        async_checks = {k: v for k, v in async_checks.items() if k in checks}
    
    # Combine all checks
    all_checks = {**sync_checks, **async_checks}
    
    if not all_checks:
        return {
            "status": "ok",
            "checks": {},
            "details": {} if include_details else None,
            "summary": {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "duration": 0.0
            }
        }
    
    start_time = time.time()
    
    # Run all checks in parallel
    tasks = [
        _run_single_check(name, func, timeout)
        for name, func in all_checks.items()
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Process results
    check_results = {}
    details = {}
    passed = 0
    failed = 0
    
    for result in results:
        if isinstance(result, Exception):
            # Handle unexpected errors in gather
            check_results["unknown"] = "fail"
            if include_details:
                details["unknown"] = f"Unexpected error: {str(result)}"
            failed += 1
        else:
            check_results[result["name"]] = result["status"]
            if result["status"] == "ok":
                passed += 1
            else:
                failed += 1
                if include_details and result["message"]:
                    details[result["name"]] = result["message"]
    
    total_duration = time.time() - start_time
    overall_status = "ok" if failed == 0 else "fail"
    
    response = {
        "status": overall_status,
        "checks": check_results,
        "summary": {
            "total": len(all_checks),
            "passed": passed,
            "failed": failed,
            "duration": total_duration
        }
    }
    
    if include_details and details:
        response["details"] = details
    
    return response


def run_health_checks_sync(
    checks: Optional[List[str]] = None,
    timeout: float = 5.0,
    include_details: bool = True
) -> Dict[str, Any]:
    """Synchronous wrapper for run_health_checks.
    
    Args:
        checks: Optional list of specific check names to run
        timeout: Timeout in seconds for each check
        include_details: Whether to include detailed error messages
        
    Returns:
        Dictionary with overall status and individual check results
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(
        run_health_checks(checks, timeout, include_details)
    )
