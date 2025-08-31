"""
Django integration for py-healthcheck.
"""

import json
from typing import Dict, List, Optional

from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from ..core import run_health_checks_sync


@require_http_methods(["GET"])
def healthcheck_view(
    request,
    checks: Optional[List[str]] = None,
    timeout: float = 5.0,
    include_details: bool = True
) -> HttpResponse:
    """Django view function for health checks.
    
    Args:
        request: Django request object
        checks: Optional list of specific check names to run
        timeout: Timeout in seconds for each check
        include_details: Whether to include detailed error messages
        
    Returns:
        Django HttpResponse with health check results
        
    Example:
        # In urls.py
        from django.urls import path
        from py_healthcheck.integrations import healthcheck_view
        
        urlpatterns = [
            path('health/', healthcheck_view, name='health_check'),
        ]
        
        # Or with specific checks
        from functools import partial
        health_check_with_checks = partial(healthcheck_view, checks=["database", "redis"])
        urlpatterns = [
            path('health/', health_check_with_checks, name='health_check'),
        ]
    """
    try:
        result = run_health_checks_sync(
            checks=checks,
            timeout=timeout,
            include_details=include_details
        )
        
        status_code = 200 if result["status"] == "ok" else 503
        
        return JsonResponse(
            result,
            status=status_code
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
        
        return JsonResponse(
            error_result,
            status=503
        )
