#!/usr/bin/env python3
"""
Basic usage example for py-healthcheck.

This example demonstrates how to use py-healthcheck for basic health checking.
"""

import asyncio
from py_healthcheck import healthcheck, run_health_checks_sync, run_health_checks
from py_healthcheck.exceptions import HealthCheckError


# Example 1: Simple synchronous health check
@healthcheck("simple_check")
def simple_health_check():
    """A simple health check that always passes."""
    return "ok"


# Example 2: Health check that can fail
@healthcheck("conditional_check")
def conditional_health_check():
    """A health check that can fail based on some condition."""
    import random
    
    if random.random() > 0.5:
        return "ok"
    else:
        raise HealthCheckError("Random failure occurred")


# Example 3: Asynchronous health check
@healthcheck("async_check")
async def async_health_check():
    """An asynchronous health check."""
    await asyncio.sleep(0.1)  # Simulate some async work
    return "ok"


# Example 4: Health check with external dependency simulation
@healthcheck("external_service")
def external_service_check():
    """Simulate checking an external service."""
    import random
    
    # Simulate network call
    if random.random() > 0.3:
        return "ok"
    else:
        raise HealthCheckError("External service is down")


def main():
    """Run the health check examples."""
    print("=== py-healthcheck Basic Usage Example ===\n")
    
    # Run synchronous health checks
    print("1. Running synchronous health checks:")
    result = run_health_checks_sync()
    print(f"Status: {result['status']}")
    print(f"Checks: {result['checks']}")
    if result.get('details'):
        print(f"Details: {result['details']}")
    print(f"Summary: {result['summary']}")
    print()
    
    # Run asynchronous health checks
    print("2. Running asynchronous health checks:")
    result = asyncio.run(run_health_checks())
    print(f"Status: {result['status']}")
    print(f"Checks: {result['checks']}")
    if result.get('details'):
        print(f"Details: {result['details']}")
    print(f"Summary: {result['summary']}")
    print()
    
    # Run specific checks only
    print("3. Running specific checks only:")
    result = run_health_checks_sync(checks=["simple_check", "async_check"])
    print(f"Status: {result['status']}")
    print(f"Checks: {result['checks']}")
    print(f"Summary: {result['summary']}")
    print()
    
    # Run with custom timeout
    print("4. Running with custom timeout:")
    result = run_health_checks_sync(timeout=1.0)
    print(f"Status: {result['status']}")
    print(f"Checks: {result['checks']}")
    print(f"Summary: {result['summary']}")
    print()
    
    # Run without details
    print("5. Running without details:")
    result = run_health_checks_sync(include_details=False)
    print(f"Status: {result['status']}")
    print(f"Checks: {result['checks']}")
    print(f"Details included: {'details' in result}")
    print(f"Summary: {result['summary']}")


if __name__ == "__main__":
    main()
