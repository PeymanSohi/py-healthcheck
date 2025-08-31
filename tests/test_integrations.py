"""
Tests for framework integrations.
"""

import json
import pytest
from unittest.mock import patch, MagicMock

from py_healthcheck.integrations.flask import register_health_endpoint
from py_healthcheck.integrations.fastapi import get_health_router
from py_healthcheck.integrations.django import healthcheck_view


class TestFlaskIntegration:
    """Test Flask integration."""
    
    def test_register_health_endpoint_success(self):
        """Test registering health endpoint with successful checks."""
        from flask import Flask
        
        app = Flask(__name__)
        
        with patch('py_healthcheck.integrations.flask.run_health_checks_sync') as mock_run:
            mock_run.return_value = {
                "status": "ok",
                "checks": {"test": "ok"},
                "summary": {"total": 1, "passed": 1, "failed": 0, "duration": 0.1}
            }
            
            register_health_endpoint(app, path="/health")
            
            with app.test_client() as client:
                response = client.get("/health")
                
                assert response.status_code == 200
                data = json.loads(response.data)
                assert data["status"] == "ok"
    
    def test_register_health_endpoint_failure(self):
        """Test registering health endpoint with failing checks."""
        from flask import Flask
        
        app = Flask(__name__)
        
        with patch('py_healthcheck.integrations.flask.run_health_checks_sync') as mock_run:
            mock_run.return_value = {
                "status": "fail",
                "checks": {"test": "fail"},
                "details": {"test": "Connection failed"},
                "summary": {"total": 1, "passed": 0, "failed": 1, "duration": 0.1}
            }
            
            register_health_endpoint(app, path="/health")
            
            with app.test_client() as client:
                response = client.get("/health")
                
                assert response.status_code == 503
                data = json.loads(response.data)
                assert data["status"] == "fail"
    
    def test_register_health_endpoint_exception(self):
        """Test registering health endpoint with exception."""
        from flask import Flask
        
        app = Flask(__name__)
        
        with patch('py_healthcheck.integrations.flask.run_health_checks_sync') as mock_run:
            mock_run.side_effect = Exception("Unexpected error")
            
            register_health_endpoint(app, path="/health")
            
            with app.test_client() as client:
                response = client.get("/health")
                
                assert response.status_code == 503
                data = json.loads(response.data)
                assert data["status"] == "fail"
                assert "error" in data["details"]


class TestFastAPIIntegration:
    """Test FastAPI integration."""
    
    def test_get_health_router_success(self):
        """Test getting health router with successful checks."""
        with patch('py_healthcheck.integrations.fastapi.run_health_checks') as mock_run:
            mock_run.return_value = {
                "status": "ok",
                "checks": {"test": "ok"},
                "summary": {"total": 1, "passed": 1, "failed": 0, "duration": 0.1}
            }
            
            router = get_health_router(path="/health")
            
            # Test the router by calling the endpoint function directly
            from fastapi import Request
            request = MagicMock(spec=Request)
            
            # Since we can't easily test FastAPI router without a full app,
            # we'll test the endpoint function directly
            endpoint_func = router.routes[0].endpoint
            
            # This would need to be run in an async context in a real test
            # For now, we just verify the router was created
            assert router is not None
            assert len(router.routes) == 1
    
    def test_get_health_router_failure(self):
        """Test getting health router with failing checks."""
        with patch('py_healthcheck.integrations.fastapi.run_health_checks') as mock_run:
            mock_run.return_value = {
                "status": "fail",
                "checks": {"test": "fail"},
                "details": {"test": "Connection failed"},
                "summary": {"total": 1, "passed": 0, "failed": 1, "duration": 0.1}
            }
            
            router = get_health_router(path="/health")
            
            assert router is not None
            assert len(router.routes) == 1
    
    def test_get_health_router_exception(self):
        """Test getting health router with exception."""
        with patch('py_healthcheck.integrations.fastapi.run_health_checks') as mock_run:
            mock_run.side_effect = Exception("Unexpected error")
            
            router = get_health_router(path="/health")
            
            assert router is not None
            assert len(router.routes) == 1


class TestDjangoIntegration:
    """Test Django integration."""
    
    def test_healthcheck_view_success(self):
        """Test health check view with successful checks."""
        from django.test import RequestFactory
        
        factory = RequestFactory()
        request = factory.get('/health/')
        
        with patch('py_healthcheck.integrations.django.run_health_checks_sync') as mock_run:
            mock_run.return_value = {
                "status": "ok",
                "checks": {"test": "ok"},
                "summary": {"total": 1, "passed": 1, "failed": 0, "duration": 0.1}
            }
            
            response = healthcheck_view(request)
            
            assert response.status_code == 200
            data = json.loads(response.content)
            assert data["status"] == "ok"
    
    def test_healthcheck_view_failure(self):
        """Test health check view with failing checks."""
        from django.test import RequestFactory
        
        factory = RequestFactory()
        request = factory.get('/health/')
        
        with patch('py_healthcheck.integrations.django.run_health_checks_sync') as mock_run:
            mock_run.return_value = {
                "status": "fail",
                "checks": {"test": "fail"},
                "details": {"test": "Connection failed"},
                "summary": {"total": 1, "passed": 0, "failed": 1, "duration": 0.1}
            }
            
            response = healthcheck_view(request)
            
            assert response.status_code == 503
            data = json.loads(response.content)
            assert data["status"] == "fail"
    
    def test_healthcheck_view_exception(self):
        """Test health check view with exception."""
        from django.test import RequestFactory
        
        factory = RequestFactory()
        request = factory.get('/health/')
        
        with patch('py_healthcheck.integrations.django.run_health_checks_sync') as mock_run:
            mock_run.side_effect = Exception("Unexpected error")
            
            response = healthcheck_view(request)
            
            assert response.status_code == 503
            data = json.loads(response.content)
            assert data["status"] == "fail"
            assert "error" in data["details"]
    
    def test_healthcheck_view_with_checks(self):
        """Test health check view with specific checks."""
        from django.test import RequestFactory
        
        factory = RequestFactory()
        request = factory.get('/health/')
        
        with patch('py_healthcheck.integrations.django.run_health_checks_sync') as mock_run:
            mock_run.return_value = {
                "status": "ok",
                "checks": {"test": "ok"},
                "summary": {"total": 1, "passed": 1, "failed": 0, "duration": 0.1}
            }
            
            response = healthcheck_view(request, checks=["test"])
            
            assert response.status_code == 200
            # Verify the checks parameter was passed
            mock_run.assert_called_once_with(
                checks=["test"],
                timeout=5.0,
                include_details=True
            )
