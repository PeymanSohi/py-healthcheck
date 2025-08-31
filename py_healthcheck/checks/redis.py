"""
Redis health checks.
"""

import asyncio
from typing import Optional

from ..exceptions import ConnectionError, HealthCheckError


def check_redis(
    connection_string: Optional[str] = None,
    host: str = "localhost",
    port: int = 6379,
    password: Optional[str] = None,
    db: int = 0,
    timeout: float = 5.0
) -> None:
    """Check Redis connection.
    
    Args:
        connection_string: Redis connection string (e.g., redis://user:pass@host:port/db)
        host: Redis host
        port: Redis port
        password: Redis password
        db: Redis database number
        timeout: Connection timeout in seconds
        
    Raises:
        HealthCheckError: If the Redis connection fails
    """
    try:
        import redis
    except ImportError:
        raise HealthCheckError("redis is required for Redis checks. Install with: pip install redis")
    
    if connection_string:
        try:
            r = redis.from_url(connection_string, socket_timeout=timeout)
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Redis: {str(e)}")
    else:
        try:
            r = redis.Redis(
                host=host,
                port=port,
                password=password,
                db=db,
                socket_timeout=timeout
            )
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Redis: {str(e)}")
    
    try:
        # Test connection with ping
        r.ping()
    except Exception as e:
        raise HealthCheckError(f"Redis health check failed: {str(e)}")
    finally:
        r.close()


async def check_redis_async(
    connection_string: Optional[str] = None,
    host: str = "localhost",
    port: int = 6379,
    password: Optional[str] = None,
    db: int = 0,
    timeout: float = 5.0
) -> None:
    """Check Redis connection asynchronously.
    
    Args:
        connection_string: Redis connection string (e.g., redis://user:pass@host:port/db)
        host: Redis host
        port: Redis port
        password: Redis password
        db: Redis database number
        timeout: Connection timeout in seconds
        
    Raises:
        HealthCheckError: If the Redis connection fails
    """
    try:
        import aioredis
    except ImportError:
        raise HealthCheckError("aioredis is required for async Redis checks. Install with: pip install aioredis")
    
    if connection_string:
        try:
            r = await asyncio.wait_for(
                aioredis.from_url(connection_string),
                timeout=timeout
            )
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Redis: {str(e)}")
    else:
        try:
            r = await asyncio.wait_for(
                aioredis.Redis(
                    host=host,
                    port=port,
                    password=password,
                    db=db,
                    socket_timeout=timeout
                ),
                timeout=timeout
            )
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Redis: {str(e)}")
    
    try:
        # Test connection with ping
        await r.ping()
    except Exception as e:
        raise HealthCheckError(f"Redis health check failed: {str(e)}")
    finally:
        await r.close()
