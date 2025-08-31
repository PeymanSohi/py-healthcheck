"""
Framework integrations for py-healthcheck.

This module provides ready-to-use integrations for popular Python web frameworks
like Flask, FastAPI, and Django.
"""

try:
    from .flask import register_health_endpoint
except ImportError:
    register_health_endpoint = None

try:
    from .fastapi import get_health_router
except ImportError:
    get_health_router = None

try:
    from .django import healthcheck_view
except ImportError:
    healthcheck_view = None

__all__ = [
    "register_health_endpoint",
    "get_health_router", 
    "healthcheck_view",
]
