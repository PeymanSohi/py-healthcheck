"""
Tests for core health check functionality.
"""

import asyncio
import pytest
import time

from py_healthcheck.core import (
    HealthCheckRegistry,
    healthcheck,
    register_health_check,
    unregister_health_check,
    run_health_checks,
    run_health_checks_sync,
)
from py_healthcheck.exceptions import HealthCheckError


class TestHealthCheckRegistry:
    """Test the health check registry."""
    
    def test_register_sync_check(self):
        """Test registering a synchronous health check."""
        registry = HealthCheckRegistry()
        
        def test_check():
            return "ok"
        
        registry.register("test", test_check)
        assert "test" in registry.get_checks()
        assert "test" not in registry.get_async_checks()
    
    def test_register_async_check(self):
        """Test registering an asynchronous health check."""
        registry = HealthCheckRegistry()
        
        async def test_check():
            return "ok"
        
        registry.register("test", test_check)
        assert "test" in registry.get_async_checks()
        assert "test" not in registry.get_checks()
    
    def test_unregister_check(self):
        """Test unregistering a health check."""
        registry = HealthCheckRegistry()
        
        def test_check():
            return "ok"
        
        registry.register("test", test_check)
        assert "test" in registry.get_checks()
        
        registry.unregister("test")
        assert "test" not in registry.get_checks()
    
    def test_clear_checks(self):
        """Test clearing all checks."""
        registry = HealthCheckRegistry()
        
        def test_check():
            return "ok"
        
        registry.register("test1", test_check)
        registry.register("test2", test_check)
        
        assert len(registry.get_checks()) == 2
        
        registry.clear()
        assert len(registry.get_checks()) == 0
        assert len(registry.get_async_checks()) == 0


class TestHealthCheckDecorator:
    """Test the health check decorator."""
    
    def test_healthcheck_decorator_sync(self):
        """Test the healthcheck decorator with sync function."""
        @healthcheck("decorated_sync")
        def test_check():
            return "ok"
        
        # The function should still be callable
        assert test_check() == "ok"
    
    def test_healthcheck_decorator_async(self):
        """Test the healthcheck decorator with async function."""
        @healthcheck("decorated_async")
        async def test_check():
            return "ok"
        
        # The function should still be callable
        result = asyncio.run(test_check())
        assert result == "ok"


class TestHealthCheckExecution:
    """Test health check execution."""
    
    def test_run_single_sync_check(self):
        """Test running a single synchronous check."""
        def test_check():
            return "ok"
        
        register_health_check("test_sync", test_check)
        
        result = run_health_checks_sync(checks=["test_sync"])
        
        assert result["status"] == "ok"
        assert result["checks"]["test_sync"] == "ok"
        assert result["summary"]["total"] == 1
        assert result["summary"]["passed"] == 1
        assert result["summary"]["failed"] == 0
    
    def test_run_single_async_check(self):
        """Test running a single asynchronous check."""
        async def test_check():
            return "ok"
        
        register_health_check("test_async", test_check)
        
        result = asyncio.run(run_health_checks(checks=["test_async"]))
        
        assert result["status"] == "ok"
        assert result["checks"]["test_async"] == "ok"
        assert result["summary"]["total"] == 1
        assert result["summary"]["passed"] == 1
        assert result["summary"]["failed"] == 0
    
    def test_run_multiple_checks(self):
        """Test running multiple checks."""
        def test_check1():
            return "ok"
        
        def test_check2():
            return "ok"
        
        register_health_check("test1", test_check1)
        register_health_check("test2", test_check2)
        
        result = run_health_checks_sync()
        
        assert result["status"] == "ok"
        assert result["checks"]["test1"] == "ok"
        assert result["checks"]["test2"] == "ok"
        assert result["summary"]["total"] == 2
        assert result["summary"]["passed"] == 2
        assert result["summary"]["failed"] == 0
    
    def test_run_check_with_failure(self):
        """Test running a check that fails."""
        def failing_check():
            raise HealthCheckError("Test failure")
        
        register_health_check("failing", failing_check)
        
        result = run_health_checks_sync(checks=["failing"])
        
        assert result["status"] == "fail"
        assert result["checks"]["failing"] == "fail"
        assert result["summary"]["total"] == 1
        assert result["summary"]["passed"] == 0
        assert result["summary"]["failed"] == 1
        assert "failing" in result["details"]
        assert "Test failure" in result["details"]["failing"]
    
    def test_run_check_with_timeout(self):
        """Test running a check that times out."""
        def slow_check():
            time.sleep(10)  # This should timeout
            return "ok"
        
        register_health_check("slow", slow_check)
        
        result = run_health_checks_sync(checks=["slow"], timeout=0.1)
        
        assert result["status"] == "fail"
        assert result["checks"]["slow"] == "fail"
        assert result["summary"]["total"] == 1
        assert result["summary"]["passed"] == 0
        assert result["summary"]["failed"] == 1
        assert "slow" in result["details"]
        assert "timed out" in result["details"]["slow"]
    
    def test_run_specific_checks(self):
        """Test running only specific checks."""
        def test_check1():
            return "ok"
        
        def test_check2():
            return "ok"
        
        register_health_check("test1", test_check1)
        register_health_check("test2", test_check2)
        
        result = run_health_checks_sync(checks=["test1"])
        
        assert result["status"] == "ok"
        assert "test1" in result["checks"]
        assert "test2" not in result["checks"]
        assert result["summary"]["total"] == 1
    
    def test_run_no_checks(self):
        """Test running when no checks are registered."""
        result = run_health_checks_sync()
        
        assert result["status"] == "ok"
        assert result["checks"] == {}
        assert result["summary"]["total"] == 0
        assert result["summary"]["passed"] == 0
        assert result["summary"]["failed"] == 0
    
    def test_run_check_with_unexpected_error(self):
        """Test running a check that raises an unexpected error."""
        def error_check():
            raise ValueError("Unexpected error")
        
        register_health_check("error", error_check)
        
        result = run_health_checks_sync(checks=["error"])
        
        assert result["status"] == "fail"
        assert result["checks"]["error"] == "fail"
        assert result["summary"]["total"] == 1
        assert result["summary"]["passed"] == 0
        assert result["summary"]["failed"] == 1
        assert "error" in result["details"]
        assert "Unexpected error" in result["details"]["error"]
    
    def test_include_details_false(self):
        """Test running checks without including details."""
        def failing_check():
            raise HealthCheckError("Test failure")
        
        register_health_check("failing", failing_check)
        
        result = run_health_checks_sync(checks=["failing"], include_details=False)
        
        assert result["status"] == "fail"
        assert result["checks"]["failing"] == "fail"
        assert "details" not in result
    
    def teardown_method(self):
        """Clean up after each test."""
        from py_healthcheck.core import _registry
        _registry.clear()
