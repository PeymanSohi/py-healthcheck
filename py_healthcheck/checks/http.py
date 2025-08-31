"""
HTTP endpoint health checks.
"""

import asyncio
from typing import Dict, Optional, Union

from ..exceptions import ConnectionError, HealthCheckError


def check_http(
    url: str,
    method: str = "GET",
    headers: Optional[Dict[str, str]] = None,
    timeout: float = 5.0,
    expected_status: Union[int, range] = 200,
    expected_content: Optional[str] = None
) -> None:
    """Check HTTP endpoint.
    
    Args:
        url: URL to check
        method: HTTP method to use
        headers: Optional headers to send
        timeout: Request timeout in seconds
        expected_status: Expected HTTP status code or range
        expected_content: Optional expected content in response body
        
    Raises:
        HealthCheckError: If the HTTP check fails
    """
    try:
        import requests
    except ImportError:
        raise HealthCheckError("requests is required for HTTP checks. Install with: pip install requests")
    
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers or {},
            timeout=timeout
        )
        
        # Check status code
        if isinstance(expected_status, int):
            if response.status_code != expected_status:
                raise HealthCheckError(f"Expected status {expected_status}, got {response.status_code}")
        elif isinstance(expected_status, range):
            if response.status_code not in expected_status:
                raise HealthCheckError(f"Expected status in {expected_status}, got {response.status_code}")
        
        # Check content if specified
        if expected_content and expected_content not in response.text:
            raise HealthCheckError(f"Expected content '{expected_content}' not found in response")
            
    except requests.exceptions.Timeout:
        raise HealthCheckError(f"HTTP request to {url} timed out after {timeout} seconds")
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError(f"Failed to connect to {url}: {str(e)}")
    except requests.exceptions.RequestException as e:
        raise HealthCheckError(f"HTTP request to {url} failed: {str(e)}")


async def check_http_async(
    url: str,
    method: str = "GET",
    headers: Optional[Dict[str, str]] = None,
    timeout: float = 5.0,
    expected_status: Union[int, range] = 200,
    expected_content: Optional[str] = None
) -> None:
    """Check HTTP endpoint asynchronously.
    
    Args:
        url: URL to check
        method: HTTP method to use
        headers: Optional headers to send
        timeout: Request timeout in seconds
        expected_status: Expected HTTP status code or range
        expected_content: Optional expected content in response body
        
    Raises:
        HealthCheckError: If the HTTP check fails
    """
    try:
        import httpx
    except ImportError:
        raise HealthCheckError("httpx is required for async HTTP checks. Install with: pip install httpx")
    
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.request(
                method=method,
                url=url,
                headers=headers or {}
            )
            
            # Check status code
            if isinstance(expected_status, int):
                if response.status_code != expected_status:
                    raise HealthCheckError(f"Expected status {expected_status}, got {response.status_code}")
            elif isinstance(expected_status, range):
                if response.status_code not in expected_status:
                    raise HealthCheckError(f"Expected status in {expected_status}, got {response.status_code}")
            
            # Check content if specified
            if expected_content and expected_content not in response.text:
                raise HealthCheckError(f"Expected content '{expected_content}' not found in response")
                
    except httpx.TimeoutException:
        raise HealthCheckError(f"HTTP request to {url} timed out after {timeout} seconds")
    except httpx.ConnectError as e:
        raise ConnectionError(f"Failed to connect to {url}: {str(e)}")
    except httpx.RequestError as e:
        raise HealthCheckError(f"HTTP request to {url} failed: {str(e)}")
