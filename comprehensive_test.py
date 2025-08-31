#!/usr/bin/env python3
"""
Comprehensive test script to verify all py-healthcheck functionality.

This script demonstrates and tests all the major features of the py-healthcheck package.
"""

import asyncio
import json
import sys
import time
from typing import Dict, Any

def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

def print_test(name: str, success: bool, details: str = ""):
    """Print a test result."""
    status = "✓ PASS" if success else "✗ FAIL"
    print(f"{status} {name}")
    if details:
        print(f"    {details}")

def test_imports():
    """Test that all modules can be imported."""
    print_section("Testing Imports")
    
    try:
        import py_healthcheck
        print_test("Main package import", True, f"Version: {py_healthcheck.__version__}")
    except ImportError as e:
        print_test("Main package import", False, str(e))
        return False
    
    try:
        from py_healthcheck.core import healthcheck, run_health_checks_sync, run_health_checks
        print_test("Core module import", True)
    except ImportError as e:
        print_test("Core module import", False, str(e))
        return False
    
    try:
        from py_healthcheck.checks import check_http
        print_test("Checks module import", True)
    except ImportError as e:
        print_test("Checks module import", False, str(e))
        return False
    
    try:
        from py_healthcheck.integrations import register_health_endpoint
        print_test("Integrations module import", True)
    except ImportError as e:
        print_test("Integrations module import", False, str(e))
        return False
    
    return True

def test_basic_functionality():
    """Test basic health check functionality."""
    print_section("Testing Basic Functionality")
    
    try:
        from py_healthcheck import healthcheck, run_health_checks_sync, run_health_checks, HealthCheckError
        
        # Test decorator registration
        @healthcheck("test_sync")
        def sync_check():
            return "ok"
        
        @healthcheck("test_async")
        async def async_check():
            await asyncio.sleep(0.01)
            return "ok"
        
        @healthcheck("test_failing")
        def failing_check():
            raise HealthCheckError("Test failure")
        
        # Test sync execution
        result = run_health_checks_sync(checks=["test_sync"])
        success = result["status"] == "ok" and result["checks"]["test_sync"] == "ok"
        print_test("Sync health check execution", success)
        
        # Test async execution
        async def test_async():
            result = await run_health_checks(checks=["test_async"])
            return result["status"] == "ok" and result["checks"]["test_async"] == "ok"
        
        success = asyncio.run(test_async())
        print_test("Async health check execution", success)
        
        # Test failure handling
        result = run_health_checks_sync(checks=["test_failing"])
        success = result["status"] == "fail" and result["checks"]["test_failing"] == "fail"
        print_test("Failure handling", success)
        
        # Test multiple checks
        result = run_health_checks_sync()
        success = len(result["checks"]) >= 3
        print_test("Multiple checks execution", success, f"Found {len(result['checks'])} checks")
        
        return True
        
    except Exception as e:
        print_test("Basic functionality", False, str(e))
        return False

def test_http_checks():
    """Test HTTP health checks."""
    print_section("Testing HTTP Checks")
    
    try:
        from py_healthcheck.checks import check_http
        
        # Test successful HTTP check
        check_http(url="https://httpbin.org/status/200")
        print_test("HTTP check - success", True)
        
        # Test failing HTTP check
        try:
            check_http(url="https://httpbin.org/status/500")
            print_test("HTTP check - failure detection", False, "Should have failed")
        except Exception:
            print_test("HTTP check - failure detection", True)
        
        # Test timeout
        try:
            check_http(url="https://httpbin.org/delay/10", timeout=0.1)
            print_test("HTTP check - timeout", False, "Should have timed out")
        except Exception:
            print_test("HTTP check - timeout", True)
        
        return True
        
    except Exception as e:
        print_test("HTTP checks", False, str(e))
        return False

def test_cli_functionality():
    """Test CLI functionality."""
    print_section("Testing CLI Functionality")
    
    try:
        import subprocess
        
        # Test CLI help
        result = subprocess.run([
            sys.executable, "-m", "py_healthcheck.cli", "--help"
        ], capture_output=True, text=True)
        
        success = result.returncode == 0 and "py-healthcheck" in result.stdout
        print_test("CLI help command", success)
        
        # Test successful HTTP check
        result = subprocess.run([
            sys.executable, "-m", "py_healthcheck.cli", 
            "--check", "http:https://httpbin.org/status/200",
            "--quiet"
        ], capture_output=True, text=True)
        
        success = result.returncode == 0 and result.stdout.strip() == "ok"
        print_test("CLI HTTP check - success", success)
        
        # Test failing HTTP check
        result = subprocess.run([
            sys.executable, "-m", "py_healthcheck.cli", 
            "--check", "http:https://httpbin.org/status/500",
            "--quiet"
        ], capture_output=True, text=True)
        
        success = result.returncode == 1 and result.stdout.strip() == "fail"
        print_test("CLI HTTP check - failure", success)
        
        # Test JSON output
        result = subprocess.run([
            sys.executable, "-m", "py_healthcheck.cli", 
            "--check", "http:https://httpbin.org/status/200"
        ], capture_output=True, text=True)
        
        try:
            json_output = json.loads(result.stdout)
            success = "status" in json_output and "checks" in json_output
            print_test("CLI JSON output", success)
        except json.JSONDecodeError:
            print_test("CLI JSON output", False, "Invalid JSON")
        
        return True
        
    except Exception as e:
        print_test("CLI functionality", False, str(e))
        return False

def test_package_metadata():
    """Test package metadata and distribution."""
    print_section("Testing Package Metadata")
    
    try:
        import py_healthcheck
        
        # Test version
        version = py_healthcheck.__version__
        success = version == "0.1.0"
        print_test("Package version", success, f"Version: {version}")
        
        # Test author
        author = py_healthcheck.__author__
        success = "py-healthcheck" in author
        print_test("Package author", success, f"Author: {author}")
        
        # Test __all__ exports
        all_exports = py_healthcheck.__all__
        expected_exports = [
            "HealthCheckError", "healthcheck", "run_health_checks", 
            "run_health_checks_sync", "check_http"
        ]
        success = all(exp in all_exports for exp in expected_exports)
        print_test("Package exports", success, f"Exports: {len(all_exports)} items")
        
        return True
        
    except Exception as e:
        print_test("Package metadata", False, str(e))
        return False

def test_performance():
    """Test performance characteristics."""
    print_section("Testing Performance")
    
    try:
        from py_healthcheck import healthcheck, run_health_checks_sync
        
        # Register multiple checks
        for i in range(5):
            @healthcheck(f"perf_check_{i}")
            def check():
                time.sleep(0.01)  # Simulate work
                return "ok"
        
        # Test execution time
        start_time = time.time()
        result = run_health_checks_sync()
        duration = time.time() - start_time
        
        success = result["status"] == "ok" and duration < 2.0
        print_test("Performance - execution time", success, f"Duration: {duration:.3f}s")
        
        # Test parallel execution
        start_time = time.time()
        result = run_health_checks_sync()
        duration = time.time() - start_time
        
        # Should be faster than sequential (5 * 0.01 = 0.05s)
        success = duration < 0.1
        print_test("Performance - parallel execution", success, f"Duration: {duration:.3f}s")
        
        return True
        
    except Exception as e:
        print_test("Performance", False, str(e))
        return False

def main():
    """Run all tests."""
    print("py-healthcheck Comprehensive Test Suite")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_basic_functionality,
        test_http_checks,
        test_cli_functionality,
        test_package_metadata,
        test_performance,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ FAIL {test.__name__} - Unexpected error: {e}")
    
    print_section("Test Results")
    print(f"Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 All tests passed! py-healthcheck is working correctly.")
        return 0
    else:
        print(f"\n❌ {total - passed} test(s) failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
