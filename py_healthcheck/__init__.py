"""
py-healthcheck: A comprehensive health check library for Python applications.

This package provides easy-to-use health checks for Python applications and microservices,
supporting both synchronous and asynchronous operations with built-in checks for common
services and framework integrations.
"""

from .core import HealthCheckError, healthcheck, run_health_checks, run_health_checks_sync
from .checks import (
    check_postgres,
    check_mysql,
    check_redis,
    check_mongodb,
    check_elasticsearch,
    check_http,
)

__version__ = "0.1.0"
__author__ = "py-healthcheck contributors"
__email__ = "info@py-healthcheck.dev"

__all__ = [
    "HealthCheckError",
    "healthcheck",
    "run_health_checks",
    "run_health_checks_sync",
    "check_postgres",
    "check_mysql",
    "check_redis",
    "check_mongodb",
    "check_elasticsearch",
    "check_http",
]
