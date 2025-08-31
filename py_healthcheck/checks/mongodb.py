"""
MongoDB health checks.
"""

import asyncio
from typing import Optional

from ..exceptions import ConnectionError, HealthCheckError


def check_mongodb(
    connection_string: Optional[str] = None,
    host: str = "localhost",
    port: int = 27017,
    database: str = "admin",
    username: Optional[str] = None,
    password: Optional[str] = None,
    timeout: float = 5.0
) -> None:
    """Check MongoDB connection.
    
    Args:
        connection_string: MongoDB connection string (e.g., mongodb://user:pass@host:port/db)
        host: MongoDB host
        port: MongoDB port
        database: Database name
        username: MongoDB username
        password: MongoDB password
        timeout: Connection timeout in seconds
        
    Raises:
        HealthCheckError: If the MongoDB connection fails
    """
    try:
        import pymongo
    except ImportError:
        raise HealthCheckError("pymongo is required for MongoDB checks. Install with: pip install pymongo")
    
    if connection_string:
        try:
            client = pymongo.MongoClient(
                connection_string,
                serverSelectionTimeoutMS=int(timeout * 1000)
            )
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MongoDB: {str(e)}")
    else:
        try:
            client = pymongo.MongoClient(
                host=host,
                port=port,
                username=username,
                password=password,
                serverSelectionTimeoutMS=int(timeout * 1000)
            )
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MongoDB: {str(e)}")
    
    try:
        # Test connection with ping
        client.admin.command('ping')
    except Exception as e:
        raise HealthCheckError(f"MongoDB health check failed: {str(e)}")
    finally:
        client.close()


async def check_mongodb_async(
    connection_string: Optional[str] = None,
    host: str = "localhost",
    port: int = 27017,
    database: str = "admin",
    username: Optional[str] = None,
    password: Optional[str] = None,
    timeout: float = 5.0
) -> None:
    """Check MongoDB connection asynchronously.
    
    Args:
        connection_string: MongoDB connection string (e.g., mongodb://user:pass@host:port/db)
        host: MongoDB host
        port: MongoDB port
        database: Database name
        username: MongoDB username
        password: MongoDB password
        timeout: Connection timeout in seconds
        
    Raises:
        HealthCheckError: If the MongoDB connection fails
    """
    try:
        import motor.motor_asyncio
    except ImportError:
        raise HealthCheckError("motor is required for async MongoDB checks. Install with: pip install motor")
    
    if connection_string:
        try:
            client = motor.motor_asyncio.AsyncIOMotorClient(
                connection_string,
                serverSelectionTimeoutMS=int(timeout * 1000)
            )
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MongoDB: {str(e)}")
    else:
        try:
            client = motor.motor_asyncio.AsyncIOMotorClient(
                host=host,
                port=port,
                username=username,
                password=password,
                serverSelectionTimeoutMS=int(timeout * 1000)
            )
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MongoDB: {str(e)}")
    
    try:
        # Test connection with ping
        await client.admin.command('ping')
    except Exception as e:
        raise HealthCheckError(f"MongoDB health check failed: {str(e)}")
    finally:
        client.close()
