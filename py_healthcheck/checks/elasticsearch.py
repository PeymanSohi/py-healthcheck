"""
Elasticsearch health checks.
"""

import asyncio
from typing import Optional

from ..exceptions import ConnectionError, HealthCheckError


def check_elasticsearch(
    connection_string: Optional[str] = None,
    host: str = "localhost",
    port: int = 9200,
    username: Optional[str] = None,
    password: Optional[str] = None,
    timeout: float = 5.0
) -> None:
    """Check Elasticsearch connection.
    
    Args:
        connection_string: Elasticsearch connection string (e.g., http://user:pass@host:port)
        host: Elasticsearch host
        port: Elasticsearch port
        username: Elasticsearch username
        password: Elasticsearch password
        timeout: Connection timeout in seconds
        
    Raises:
        HealthCheckError: If the Elasticsearch connection fails
    """
    try:
        import elasticsearch
    except ImportError:
        raise HealthCheckError("elasticsearch is required for Elasticsearch checks. Install with: pip install elasticsearch")
    
    if connection_string:
        try:
            es = elasticsearch.Elasticsearch(
                [connection_string],
                timeout=timeout
            )
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Elasticsearch: {str(e)}")
    else:
        try:
            es = elasticsearch.Elasticsearch(
                [{"host": host, "port": port}],
                http_auth=(username, password) if username and password else None,
                timeout=timeout
            )
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Elasticsearch: {str(e)}")
    
    try:
        # Test connection with cluster health
        health = es.cluster.health()
        if health["status"] in ["red"]:
            raise HealthCheckError(f"Elasticsearch cluster is unhealthy: {health['status']}")
    except Exception as e:
        raise HealthCheckError(f"Elasticsearch health check failed: {str(e)}")


async def check_elasticsearch_async(
    connection_string: Optional[str] = None,
    host: str = "localhost",
    port: int = 9200,
    username: Optional[str] = None,
    password: Optional[str] = None,
    timeout: float = 5.0
) -> None:
    """Check Elasticsearch connection asynchronously.
    
    Args:
        connection_string: Elasticsearch connection string (e.g., http://user:pass@host:port)
        host: Elasticsearch host
        port: Elasticsearch port
        username: Elasticsearch username
        password: Elasticsearch password
        timeout: Connection timeout in seconds
        
    Raises:
        HealthCheckError: If the Elasticsearch connection fails
    """
    try:
        import elasticsearch
    except ImportError:
        raise HealthCheckError("elasticsearch is required for Elasticsearch checks. Install with: pip install elasticsearch")
    
    if connection_string:
        try:
            es = elasticsearch.AsyncElasticsearch(
                [connection_string],
                timeout=timeout
            )
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Elasticsearch: {str(e)}")
    else:
        try:
            es = elasticsearch.AsyncElasticsearch(
                [{"host": host, "port": port}],
                http_auth=(username, password) if username and password else None,
                timeout=timeout
            )
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Elasticsearch: {str(e)}")
    
    try:
        # Test connection with cluster health
        health = await es.cluster.health()
        if health["status"] in ["red"]:
            raise HealthCheckError(f"Elasticsearch cluster is unhealthy: {health['status']}")
    except Exception as e:
        raise HealthCheckError(f"Elasticsearch health check failed: {str(e)}")
    finally:
        await es.close()
