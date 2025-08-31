"""
Tests for built-in health checks.
"""

import pytest
from unittest.mock import patch, MagicMock

from py_healthcheck.checks.db import check_postgres, check_mysql
from py_healthcheck.checks.redis import check_redis
from py_healthcheck.checks.mongodb import check_mongodb
from py_healthcheck.checks.elasticsearch import check_elasticsearch
from py_healthcheck.checks.http import check_http
from py_healthcheck.exceptions import HealthCheckError, ConnectionError


class TestPostgreSQLCheck:
    """Test PostgreSQL health check."""
    
    def test_check_postgres_success(self):
        """Test successful PostgreSQL check."""
        with patch('py_healthcheck.checks.db.psycopg2') as mock_psycopg2:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_psycopg2.connect.return_value = mock_conn
            
            # Should not raise any exception
            check_postgres(connection_string="postgresql://user:pass@host/db")
            
            mock_psycopg2.connect.assert_called_once()
            mock_cursor.execute.assert_called_once_with("SELECT 1")
    
    def test_check_postgres_connection_error(self):
        """Test PostgreSQL check with connection error."""
        with patch('py_healthcheck.checks.db.psycopg2') as mock_psycopg2:
            mock_psycopg2.connect.side_effect = Exception("Connection failed")
            
            with pytest.raises(ConnectionError, match="Failed to connect to PostgreSQL"):
                check_postgres(connection_string="postgresql://user:pass@host/db")
    
    def test_check_postgres_missing_psycopg2(self):
        """Test PostgreSQL check when psycopg2 is not installed."""
        with patch('py_healthcheck.checks.db.psycopg2', side_effect=ImportError):
            with pytest.raises(HealthCheckError, match="psycopg2 is required"):
                check_postgres(connection_string="postgresql://user:pass@host/db")
    
    def test_check_postgres_missing_username(self):
        """Test PostgreSQL check without username."""
        with pytest.raises(HealthCheckError, match="Username is required"):
            check_postgres(host="localhost", port=5432)


class TestMySQLCheck:
    """Test MySQL health check."""
    
    def test_check_mysql_success(self):
        """Test successful MySQL check."""
        with patch('py_healthcheck.checks.db.pymysql') as mock_pymysql:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_pymysql.connect.return_value = mock_conn
            
            # Should not raise any exception
            check_mysql(connection_string="mysql://user:pass@host/db")
            
            mock_pymysql.connect.assert_called_once()
            mock_cursor.execute.assert_called_once_with("SELECT 1")
    
    def test_check_mysql_connection_error(self):
        """Test MySQL check with connection error."""
        with patch('py_healthcheck.checks.db.pymysql') as mock_pymysql:
            mock_pymysql.connect.side_effect = Exception("Connection failed")
            
            with pytest.raises(ConnectionError, match="Failed to connect to MySQL"):
                check_mysql(connection_string="mysql://user:pass@host/db")
    
    def test_check_mysql_missing_pymysql(self):
        """Test MySQL check when pymysql is not installed."""
        with patch('py_healthcheck.checks.db.pymysql', side_effect=ImportError):
            with pytest.raises(HealthCheckError, match="pymysql is required"):
                check_mysql(connection_string="mysql://user:pass@host/db")


class TestRedisCheck:
    """Test Redis health check."""
    
    def test_check_redis_success(self):
        """Test successful Redis check."""
        with patch('py_healthcheck.checks.redis.redis') as mock_redis:
            mock_client = MagicMock()
            mock_redis.from_url.return_value = mock_client
            
            # Should not raise any exception
            check_redis(connection_string="redis://localhost:6379")
            
            mock_redis.from_url.assert_called_once()
            mock_client.ping.assert_called_once()
    
    def test_check_redis_connection_error(self):
        """Test Redis check with connection error."""
        with patch('py_healthcheck.checks.redis.redis') as mock_redis:
            mock_redis.from_url.side_effect = Exception("Connection failed")
            
            with pytest.raises(ConnectionError, match="Failed to connect to Redis"):
                check_redis(connection_string="redis://localhost:6379")
    
    def test_check_redis_missing_redis(self):
        """Test Redis check when redis is not installed."""
        with patch('py_healthcheck.checks.redis.redis', side_effect=ImportError):
            with pytest.raises(HealthCheckError, match="redis is required"):
                check_redis(connection_string="redis://localhost:6379")


class TestMongoDBCheck:
    """Test MongoDB health check."""
    
    def test_check_mongodb_success(self):
        """Test successful MongoDB check."""
        with patch('py_healthcheck.checks.mongodb.pymongo') as mock_pymongo:
            mock_client = MagicMock()
            mock_client.admin.command.return_value = {"ok": 1}
            mock_pymongo.MongoClient.return_value = mock_client
            
            # Should not raise any exception
            check_mongodb(connection_string="mongodb://localhost:27017")
            
            mock_pymongo.MongoClient.assert_called_once()
            mock_client.admin.command.assert_called_once_with('ping')
    
    def test_check_mongodb_connection_error(self):
        """Test MongoDB check with connection error."""
        with patch('py_healthcheck.checks.mongodb.pymongo') as mock_pymongo:
            mock_pymongo.MongoClient.side_effect = Exception("Connection failed")
            
            with pytest.raises(ConnectionError, match="Failed to connect to MongoDB"):
                check_mongodb(connection_string="mongodb://localhost:27017")
    
    def test_check_mongodb_missing_pymongo(self):
        """Test MongoDB check when pymongo is not installed."""
        with patch('py_healthcheck.checks.mongodb.pymongo', side_effect=ImportError):
            with pytest.raises(HealthCheckError, match="pymongo is required"):
                check_mongodb(connection_string="mongodb://localhost:27017")


class TestElasticsearchCheck:
    """Test Elasticsearch health check."""
    
    def test_check_elasticsearch_success(self):
        """Test successful Elasticsearch check."""
        with patch('py_healthcheck.checks.elasticsearch.elasticsearch') as mock_es:
            mock_client = MagicMock()
            mock_client.cluster.health.return_value = {"status": "green"}
            mock_es.Elasticsearch.return_value = mock_client
            
            # Should not raise any exception
            check_elasticsearch(connection_string="http://localhost:9200")
            
            mock_es.Elasticsearch.assert_called_once()
            mock_client.cluster.health.assert_called_once()
    
    def test_check_elasticsearch_unhealthy_cluster(self):
        """Test Elasticsearch check with unhealthy cluster."""
        with patch('py_healthcheck.checks.elasticsearch.elasticsearch') as mock_es:
            mock_client = MagicMock()
            mock_client.cluster.health.return_value = {"status": "red"}
            mock_es.Elasticsearch.return_value = mock_client
            
            with pytest.raises(HealthCheckError, match="Elasticsearch cluster is unhealthy"):
                check_elasticsearch(connection_string="http://localhost:9200")
    
    def test_check_elasticsearch_missing_elasticsearch(self):
        """Test Elasticsearch check when elasticsearch is not installed."""
        with patch('py_healthcheck.checks.elasticsearch.elasticsearch', side_effect=ImportError):
            with pytest.raises(HealthCheckError, match="elasticsearch is required"):
                check_elasticsearch(connection_string="http://localhost:9200")


class TestHTTPCheck:
    """Test HTTP health check."""
    
    def test_check_http_success(self):
        """Test successful HTTP check."""
        with patch('py_healthcheck.checks.http.requests') as mock_requests:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.text = "OK"
            mock_requests.request.return_value = mock_response
            
            # Should not raise any exception
            check_http(url="http://localhost:8080/health")
            
            mock_requests.request.assert_called_once()
    
    def test_check_http_wrong_status(self):
        """Test HTTP check with wrong status code."""
        with patch('py_healthcheck.checks.http.requests') as mock_requests:
            mock_response = MagicMock()
            mock_response.status_code = 500
            mock_requests.request.return_value = mock_response
            
            with pytest.raises(HealthCheckError, match="Expected status 200, got 500"):
                check_http(url="http://localhost:8080/health")
    
    def test_check_http_missing_content(self):
        """Test HTTP check with missing expected content."""
        with patch('py_healthcheck.checks.http.requests') as mock_requests:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.text = "Not OK"
            mock_requests.request.return_value = mock_response
            
            with pytest.raises(HealthCheckError, match="Expected content 'OK' not found"):
                check_http(url="http://localhost:8080/health", expected_content="OK")
    
    def test_check_http_timeout(self):
        """Test HTTP check with timeout."""
        with patch('py_healthcheck.checks.http.requests') as mock_requests:
            import requests
            mock_requests.request.side_effect = requests.exceptions.Timeout()
            
            with pytest.raises(HealthCheckError, match="timed out"):
                check_http(url="http://localhost:8080/health")
    
    def test_check_http_connection_error(self):
        """Test HTTP check with connection error."""
        with patch('py_healthcheck.checks.http.requests') as mock_requests:
            import requests
            mock_requests.request.side_effect = requests.exceptions.ConnectionError()
            
            with pytest.raises(ConnectionError, match="Failed to connect"):
                check_http(url="http://localhost:8080/health")
    
    def test_check_http_missing_requests(self):
        """Test HTTP check when requests is not installed."""
        with patch('py_healthcheck.checks.http.requests', side_effect=ImportError):
            with pytest.raises(HealthCheckError, match="requests is required"):
                check_http(url="http://localhost:8080/health")
