"""
Database health checks for PostgreSQL and MySQL.
"""

import asyncio
import socket
from typing import Dict, Optional, Union

from ..exceptions import ConnectionError, HealthCheckError


def check_postgres(
    connection_string: Optional[str] = None,
    host: str = "localhost",
    port: int = 5432,
    database: str = "postgres",
    username: Optional[str] = None,
    password: Optional[str] = None,
    timeout: float = 5.0
) -> None:
    """Check PostgreSQL database connection.
    
    Args:
        connection_string: PostgreSQL connection string (e.g., postgresql://user:pass@host/db)
        host: Database host
        port: Database port
        database: Database name
        username: Database username
        password: Database password
        timeout: Connection timeout in seconds
        
    Raises:
        HealthCheckError: If the database connection fails
    """
    try:
        import psycopg2
        from psycopg2 import sql
    except ImportError:
        raise HealthCheckError("psycopg2 is required for PostgreSQL checks. Install with: pip install psycopg2-binary")
    
    if connection_string:
        try:
            conn = psycopg2.connect(connection_string, connect_timeout=timeout)
        except Exception as e:
            raise ConnectionError(f"Failed to connect to PostgreSQL: {str(e)}")
    else:
        if not username:
            raise HealthCheckError("Username is required when not using connection string")
        
        try:
            conn = psycopg2.connect(
                host=host,
                port=port,
                database=database,
                user=username,
                password=password,
                connect_timeout=timeout
            )
        except Exception as e:
            raise ConnectionError(f"Failed to connect to PostgreSQL: {str(e)}")
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except Exception as e:
        raise HealthCheckError(f"PostgreSQL health check failed: {str(e)}")
    finally:
        conn.close()


async def check_postgres_async(
    connection_string: Optional[str] = None,
    host: str = "localhost",
    port: int = 5432,
    database: str = "postgres",
    username: Optional[str] = None,
    password: Optional[str] = None,
    timeout: float = 5.0
) -> None:
    """Check PostgreSQL database connection asynchronously.
    
    Args:
        connection_string: PostgreSQL connection string (e.g., postgresql://user:pass@host/db)
        host: Database host
        port: Database port
        database: Database name
        username: Database username
        password: Database password
        timeout: Connection timeout in seconds
        
    Raises:
        HealthCheckError: If the database connection fails
    """
    try:
        import asyncpg
    except ImportError:
        raise HealthCheckError("asyncpg is required for async PostgreSQL checks. Install with: pip install asyncpg")
    
    if connection_string:
        try:
            conn = await asyncio.wait_for(
                asyncpg.connect(connection_string),
                timeout=timeout
            )
        except Exception as e:
            raise ConnectionError(f"Failed to connect to PostgreSQL: {str(e)}")
    else:
        if not username:
            raise HealthCheckError("Username is required when not using connection string")
        
        try:
            conn = await asyncio.wait_for(
                asyncpg.connect(
                    host=host,
                    port=port,
                    database=database,
                    user=username,
                    password=password
                ),
                timeout=timeout
            )
        except Exception as e:
            raise ConnectionError(f"Failed to connect to PostgreSQL: {str(e)}")
    
    try:
        await conn.fetchval("SELECT 1")
    except Exception as e:
        raise HealthCheckError(f"PostgreSQL health check failed: {str(e)}")
    finally:
        await conn.close()


def check_mysql(
    connection_string: Optional[str] = None,
    host: str = "localhost",
    port: int = 3306,
    database: str = "mysql",
    username: Optional[str] = None,
    password: Optional[str] = None,
    timeout: float = 5.0
) -> None:
    """Check MySQL database connection.
    
    Args:
        connection_string: MySQL connection string (e.g., mysql://user:pass@host/db)
        host: Database host
        port: Database port
        database: Database name
        username: Database username
        password: Database password
        timeout: Connection timeout in seconds
        
    Raises:
        HealthCheckError: If the database connection fails
    """
    try:
        import pymysql
    except ImportError:
        raise HealthCheckError("pymysql is required for MySQL checks. Install with: pip install pymysql")
    
    if connection_string:
        try:
            conn = pymysql.connect(
                connection_string,
                connect_timeout=timeout
            )
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MySQL: {str(e)}")
    else:
        if not username:
            raise HealthCheckError("Username is required when not using connection string")
        
        try:
            conn = pymysql.connect(
                host=host,
                port=port,
                database=database,
                user=username,
                password=password,
                connect_timeout=timeout
            )
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MySQL: {str(e)}")
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except Exception as e:
        raise HealthCheckError(f"MySQL health check failed: {str(e)}")
    finally:
        conn.close()


async def check_mysql_async(
    connection_string: Optional[str] = None,
    host: str = "localhost",
    port: int = 3306,
    database: str = "mysql",
    username: Optional[str] = None,
    password: Optional[str] = None,
    timeout: float = 5.0
) -> None:
    """Check MySQL database connection asynchronously.
    
    Args:
        connection_string: MySQL connection string (e.g., mysql://user:pass@host/db)
        host: Database host
        port: Database port
        database: Database name
        username: Database username
        password: Database password
        timeout: Connection timeout in seconds
        
    Raises:
        HealthCheckError: If the database connection fails
    """
    try:
        import aiomysql
    except ImportError:
        raise HealthCheckError("aiomysql is required for async MySQL checks. Install with: pip install aiomysql")
    
    if connection_string:
        try:
            conn = await asyncio.wait_for(
                aiomysql.connect(connection_string),
                timeout=timeout
            )
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MySQL: {str(e)}")
    else:
        if not username:
            raise HealthCheckError("Username is required when not using connection string")
        
        try:
            conn = await asyncio.wait_for(
                aiomysql.connect(
                    host=host,
                    port=port,
                    db=database,
                    user=username,
                    password=password
                ),
                timeout=timeout
            )
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MySQL: {str(e)}")
    
    try:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT 1")
            await cursor.fetchone()
    except Exception as e:
        raise HealthCheckError(f"MySQL health check failed: {str(e)}")
    finally:
        conn.close()
