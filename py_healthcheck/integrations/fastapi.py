"""
FastAPI integration for py-healthcheck.
"""

import json
from typing import Dict, List, Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from ..core import run_health_checks


def get_health_router(
    path: str = "/health",
    checks: Optional[List[str]] = None,
    timeout: float = 5.0,
    include_details: bool = True
) -> APIRouter:
    """Create a FastAPI router with health check endpoint.
    
    Args:
        path: URL path for the health endpoint
        checks: Optional list of specific check names to run
        timeout: Timeout in seconds for each check
        include_details: Whether to include detailed error messages
        
    Returns:
        FastAPI router with health check endpoint
        
    Example:
        from fastapi import FastAPI
        from py_healthcheck.integrations import get_health_router
        
        app = FastAPI()
        health_router = get_health_router(path="/health")
        app.include_router(health_router)
        
        # Or with specific checks
        health_router = get_health_router(path="/health", checks=["database", "redis"])
        app.include_router(health_router)
    """
    
    router = APIRouter()
    
    @router.get(path)
    async def health_check():
        """Health check endpoint handler."""
        try:
            result = await run_health_checks(
                checks=checks,
                timeout=timeout,
                include_details=include_details
            )
            
            status_code = 200 if result["status"] == "ok" else 503
            
            return JSONResponse(
                content=result,
                status_code=status_code
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
            
            return JSONResponse(
                content=error_result,
                status_code=503
            )
    
    return router
