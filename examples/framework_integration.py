#!/usr/bin/env python3
"""
Framework integration examples for py-healthcheck.

This example demonstrates how to integrate py-healthcheck with Flask, FastAPI, and Django.
"""

# Flask Example
def flask_example():
    """Example Flask integration."""
    try:
        from flask import Flask
        from py_healthcheck.integrations import register_health_endpoint
        from py_healthcheck import healthcheck
        
        @healthcheck("flask_database")
        def check_database():
            # Simulate database check
            return "ok"
        
        app = Flask(__name__)
        
        # Register health endpoint
        register_health_endpoint(app, path="/health")
        
        print("Flask app created with health endpoint at /health")
        print("Run with: flask run")
        return app
        
    except ImportError:
        print("Flask not installed. Install with: pip install flask")
        return None


# FastAPI Example
def fastapi_example():
    """Example FastAPI integration."""
    try:
        from fastapi import FastAPI
        from py_healthcheck.integrations import get_health_router
        from py_healthcheck import healthcheck
        
        @healthcheck("fastapi_database")
        def check_database():
            # Simulate database check
            return "ok"
        
        app = FastAPI()
        
        # Include health router
        health_router = get_health_router(path="/health")
        app.include_router(health_router)
        
        print("FastAPI app created with health endpoint at /health")
        print("Run with: uvicorn examples.framework_integration:fastapi_app --reload")
        return app
        
    except ImportError:
        print("FastAPI not installed. Install with: pip install fastapi uvicorn")
        return None


# Django Example
def django_example():
    """Example Django integration."""
    try:
        from django.conf import settings
        from django.urls import path
        from py_healthcheck.integrations import healthcheck_view
        from py_healthcheck import healthcheck
        
        @healthcheck("django_database")
        def check_database():
            # Simulate database check
            return "ok"
        
        # Django URL configuration
        urlpatterns = [
            path('health/', healthcheck_view, name='health_check'),
        ]
        
        print("Django URL configuration created with health endpoint at /health/")
        print("Add to your Django project's urls.py")
        return urlpatterns
        
    except ImportError:
        print("Django not installed. Install with: pip install django")
        return None


def main():
    """Run the framework integration examples."""
    print("=== py-healthcheck Framework Integration Examples ===\n")
    
    print("1. Flask Integration:")
    flask_app = flask_example()
    print()
    
    print("2. FastAPI Integration:")
    fastapi_app = fastapi_example()
    print()
    
    print("3. Django Integration:")
    django_urls = django_example()
    print()
    
    print("Note: These are example configurations.")
    print("For production use, ensure proper error handling and security measures.")


# Create FastAPI app instance for uvicorn
try:
    fastapi_app = fastapi_example()
except:
    fastapi_app = None


if __name__ == "__main__":
    main()
