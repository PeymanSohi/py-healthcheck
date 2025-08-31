"""
Built-in health checks for common services.

This module provides pre-built health checks for popular services
like databases, caches, and HTTP endpoints.
"""

from .db import check_postgres, check_mysql
from .redis import check_redis
from .mongodb import check_mongodb
from .elasticsearch import check_elasticsearch
from .http import check_http

__all__ = [
    "check_postgres",
    "check_mysql", 
    "check_redis",
    "check_mongodb",
    "check_elasticsearch",
    "check_http",
]
