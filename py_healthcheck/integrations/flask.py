"""
Flask integration for py-healthcheck.
"""

import json
from typing import Dict, List, Optional

from flask import Flask, Response

from ..core import run_health_checks_sync


def register_health_endpoint(
    app: Flask,
    path: str = "/health",
    checks: Optional[List[str]] = None,
    timeout: float = 5.0,
    include_details: bool = True
) -> None:
    """Register a health check endpoint with Flask.
    
    Args:
        app: Flask application instance
        path: URL path for the health endpoint
        checks: Optional list of specific check names to run
        timeout: Timeout in seconds for each check
        include_details: Whether to include detailed error messages
        
    Example:
        from flask import Flask
        from py_healthcheck.integrations import register_health_endpoint
        
        app = Flask(__name__)
        register_health_endpoint(app, path="/health")
        
        # Or with specific checks
        register_health_endpoint(app, path="/health", checks=["database", "redis"])
    """
    
    def health_check():
        """Health check endpoint handler."""
        try:
            result = run_health_checks_sync(
                checks=checks,
                timeout=timeout,
                include_details=include_details
            )
            
            status_code = 200 if result["status"] == "ok" else 503
            
            return Response(
                json.dumps(result, indent=2),
                status=status_code,
                mimetype="application/json"
            )
            
        except Exception as e:
            error_result = {
                "status": "fail",
                "checks": {},
                "details": {"error": str(e)},
                "summary": {
                    "total": 0,
                    "passed": 0,
                    "failed": 1,
                    "duration": 0.0
                }
            }
            
            return Response(
                json.dumps(error_result, indent=2),
                status=503,
                mimetype="application/json"
            )
    
    app.add_url_rule(path, "health_check", health_check, methods=["GET"])
