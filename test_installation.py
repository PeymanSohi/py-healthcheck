#!/usr/bin/env python3
"""
Test script to verify py-healthcheck installation and basic functionality.
"""

import sys
import traceback


def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        import py_healthcheck
        print("✓ py_healthcheck imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import py_healthcheck: {e}")
        return False
    
    try:
        from py_healthcheck.core import healthcheck, run_health_checks_sync
        print("✓ Core modules imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import core modules: {e}")
        return False
    
    try:
        from py_healthcheck.checks import check_http
        print("✓ Check modules imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import check modules: {e}")
        return False
    
    try:
        from py_healthcheck.integrations import register_health_endpoint
        print("✓ Integration modules imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import integration modules: {e}")
        return False
    
    return True


def test_basic_functionality():
    """Test basic functionality."""
    print("\nTesting basic functionality...")
    
    try:
        from py_healthcheck import healthcheck, run_health_checks_sync
        
        # Register a simple health check
        @healthcheck("test_check")
        def test_health_check():
            return "ok"
        
        # Run health checks
        result = run_health_checks_sync()
        
        if result["status"] == "ok" and "test_check" in result["checks"]:
            print("✓ Basic health check functionality works")
            return True
        else:
            print(f"✗ Health check failed: {result}")
            return False
            
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        traceback.print_exc()
        return False


def test_http_check():
    """Test HTTP check functionality."""
    print("\nTesting HTTP check...")
    
    try:
        from py_healthcheck.checks import check_http
        
        # Test with a simple HTTP endpoint
        check_http(url="https://httpbin.org/status/200")
        print("✓ HTTP check works")
        return True
        
    except Exception as e:
        print(f"✗ HTTP check failed: {e}")
        return False


def main():
    """Main test function."""
    print("=== py-healthcheck Installation Test ===\n")
    
    tests = [
        test_imports,
        test_basic_functionality,
        test_http_check,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")
            traceback.print_exc()
    
    print(f"\n=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed! py-healthcheck is working correctly.")
        return 0
    else:
        print("✗ Some tests failed. Please check the installation.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
