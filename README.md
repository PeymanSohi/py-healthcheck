# py-healthcheck

[![PyPI version](https://badge.fury.io/py/py-healthcheck.svg)](https://badge.fury.io/py/py-healthcheck)
[![Python Support](https://img.shields.io/pypi/pyversions/py-healthcheck.svg)](https://pypi.org/project/py-healthcheck/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/py-healthcheck/py-healthcheck/workflows/Tests/badge.svg)](https://github.com/py-healthcheck/py-healthcheck/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A comprehensive health check library for Python applications and microservices. Built with async support, framework integrations, and a powerful CLI tool.

## Features

- 🚀 **Async & Sync Support**: Run health checks synchronously or asynchronously
- 🔧 **Built-in Checks**: PostgreSQL, MySQL, Redis, MongoDB, Elasticsearch, HTTP endpoints
- 🎯 **Framework Integrations**: Ready-to-use integrations for Flask, FastAPI, and Django
- 🖥️ **CLI Tool**: Command-line interface for running health checks
- ⚡ **Parallel Execution**: Run multiple checks in parallel for better performance
- 🎨 **Rich Output**: Beautiful table output with colors (optional)
- 📊 **Detailed Results**: Get comprehensive status reports with timing and error details
- 🔌 **Extensible**: Easy to add custom health checks via decorators or registration

## Installation

### Basic Installation

```bash
pip install py-healthcheck
```

### With Database Support

```bash
# PostgreSQL
pip install py-healthcheck[postgres]

# MySQL
pip install py-healthcheck[mysql]

# Redis
pip install py-healthcheck[redis]

# MongoDB
pip install py-healthcheck[mongodb]

# Elasticsearch
pip install py-healthcheck[elasticsearch]
```

### With Framework Integrations

```bash
# Flask
pip install py-healthcheck[flask]

# FastAPI
pip install py-healthcheck[fastapi]

# Django
pip install py-healthcheck[django]
```

### With CLI Enhancements

```bash
# Rich table output
pip install py-healthcheck[cli]
```

### All Features

```bash
pip install py-healthcheck[all]
```

## Quick Start

### Basic Usage

```python
from py_healthcheck import healthcheck, run_health_checks_sync

# Define a custom health check
@healthcheck("database")
def check_database():
    # Your database check logic here
    pass

# Run all registered checks
result = run_health_checks_sync()
print(result)
```

### Async Usage

```python
import asyncio
from py_healthcheck import healthcheck, run_health_checks

@healthcheck("api")
async def check_api():
    # Your async API check logic here
    pass

# Run checks asynchronously
result = asyncio.run(run_health_checks())
print(result)
```

### Built-in Checks

```python
from py_healthcheck.checks import check_postgres, check_redis, check_http

# Register built-in checks
from py_healthcheck import register_health_check

register_health_check("postgres", lambda: check_postgres(
    connection_string="postgresql://user:pass@localhost/db"
))

register_health_check("redis", lambda: check_redis(
    connection_string="redis://localhost:6379"
))

register_health_check("api", lambda: check_http(
    url="http://localhost:8080/health"
))
```

## CLI Usage

### Basic Commands

```bash
# Check a PostgreSQL database
py-healthcheck --check postgres:postgresql://user:pass@localhost/mydb

# Check multiple services
py-healthcheck --check postgres:postgresql://user:pass@localhost/mydb \
               --check redis:redis://localhost:6379 \
               --check http:http://localhost:8080/health

# Use table format with verbose output
py-healthcheck --check postgres:postgresql://user:pass@localhost/mydb \
               --format table --verbose

# Set custom timeout
py-healthcheck --check postgres:postgresql://user:pass@localhost/mydb \
               --timeout 10

# Quiet mode (only output status)
py-healthcheck --check postgres:postgresql://user:pass@localhost/mydb --quiet
```

### CLI Options

- `--check TYPE:URL`: Specify a check to run (can be used multiple times)
- `--format json|table`: Output format (default: json)
- `--timeout SECONDS`: Timeout for each check (default: 5)
- `--verbose`: Include detailed information
- `--quiet`: Only output the final status

### Supported Check Types

- `postgres`: PostgreSQL database
- `mysql`: MySQL database
- `redis`: Redis cache
- `mongodb`: MongoDB database
- `elasticsearch`: Elasticsearch cluster
- `http`: HTTP endpoint

## Framework Integrations

### Flask

```python
from flask import Flask
from py_healthcheck.integrations import register_health_endpoint

app = Flask(__name__)

# Register health endpoint at /health
register_health_endpoint(app, path="/health")

# Or with specific checks
register_health_endpoint(app, path="/health", checks=["database", "redis"])
```

### FastAPI

```python
from fastapi import FastAPI
from py_healthcheck.integrations import get_health_router

app = FastAPI()

# Include health router
health_router = get_health_router(path="/health")
app.include_router(health_router)

# Or with specific checks
health_router = get_health_router(path="/health", checks=["database", "redis"])
app.include_router(health_router)
```

### Django

```python
# urls.py
from django.urls import path
from py_healthcheck.integrations import healthcheck_view

urlpatterns = [
    path('health/', healthcheck_view, name='health_check'),
]

# Or with specific checks
from functools import partial
health_check_with_checks = partial(healthcheck_view, checks=["database", "redis"])
urlpatterns = [
    path('health/', health_check_with_checks, name='health_check'),
]
```

## Built-in Health Checks

### Database Checks

#### PostgreSQL

```python
from py_healthcheck.checks import check_postgres

# Using connection string
check_postgres(connection_string="postgresql://user:pass@host/db")

# Using individual parameters
check_postgres(
    host="localhost",
    port=5432,
    database="mydb",
    username="user",
    password="pass"
)
```

#### MySQL

```python
from py_healthcheck.checks import check_mysql

# Using connection string
check_mysql(connection_string="mysql://user:pass@host/db")

# Using individual parameters
check_mysql(
    host="localhost",
    port=3306,
    database="mydb",
    username="user",
    password="pass"
)
```

### Cache Checks

#### Redis

```python
from py_healthcheck.checks import check_redis

# Using connection string
check_redis(connection_string="redis://localhost:6379")

# Using individual parameters
check_redis(
    host="localhost",
    port=6379,
    password="secret",
    db=0
)
```

### Document Database Checks

#### MongoDB

```python
from py_healthcheck.checks import check_mongodb

# Using connection string
check_mongodb(connection_string="mongodb://localhost:27017")

# Using individual parameters
check_mongodb(
    host="localhost",
    port=27017,
    database="mydb",
    username="user",
    password="pass"
)
```

### Search Engine Checks

#### Elasticsearch

```python
from py_healthcheck.checks import check_elasticsearch

# Using connection string
check_elasticsearch(connection_string="http://localhost:9200")

# Using individual parameters
check_elasticsearch(
    host="localhost",
    port=9200,
    username="user",
    password="pass"
)
```

### HTTP Checks

```python
from py_healthcheck.checks import check_http

# Basic HTTP check
check_http(url="http://localhost:8080/health")

# With custom method and headers
check_http(
    url="http://localhost:8080/health",
    method="POST",
    headers={"Authorization": "Bearer token"},
    expected_status=200,
    expected_content="OK"
)
```

## Custom Health Checks

### Using Decorators

```python
from py_healthcheck import healthcheck

@healthcheck("my_service")
def check_my_service():
    # Your health check logic
    if some_condition:
        return "ok"
    else:
        raise HealthCheckError("Service is down")

@healthcheck("async_service")
async def check_async_service():
    # Your async health check logic
    result = await some_async_operation()
    if not result:
        raise HealthCheckError("Async service failed")
```

### Programmatic Registration

```python
from py_healthcheck import register_health_check

def my_check():
    # Your check logic
    pass

register_health_check("my_check", my_check)
```

## Output Format

### JSON Output

```json
{
  "status": "ok",
  "checks": {
    "database": "ok",
    "redis": "ok",
    "api": "fail"
  },
  "details": {
    "api": "Connection timeout"
  },
  "summary": {
    "total": 3,
    "passed": 2,
    "failed": 1,
    "duration": 0.245
  }
}
```

### Table Output

```
Health Check Results
═══════════════════════════════════════════════════════════
Check      Status   Details
───────────────────────────────────────────────────────────
database   ✓ ok
redis      ✓ ok
api        ✗ fail   Connection timeout
───────────────────────────────────────────────────────────
SUMMARY    FAIL     Total: 3, Passed: 2, Failed: 1
```

## Error Handling

The library provides specific exception types for different error scenarios:

```python
from py_healthcheck.exceptions import (
    HealthCheckError,
    ConnectionError,
    TimeoutError,
    ConfigurationError
)

try:
    check_postgres(connection_string="invalid://connection")
except ConnectionError as e:
    print(f"Connection failed: {e}")
except HealthCheckError as e:
    print(f"Health check failed: {e}")
```

## Configuration

### Environment Variables

You can configure default settings using environment variables:

```bash
export PY_HEALTHCHECK_TIMEOUT=10
export PY_HEALTHCHECK_INCLUDE_DETAILS=true
```

### Programmatic Configuration

```python
from py_healthcheck import run_health_checks_sync

result = run_health_checks_sync(
    checks=["database", "redis"],  # Specific checks to run
    timeout=10.0,                  # Timeout per check
    include_details=True           # Include error details
)
```

## Development

### Setup Development Environment

```bash
git clone https://github.com/py-healthcheck/py-healthcheck.git
cd py-healthcheck
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=py_healthcheck

# Run specific test file
pytest tests/test_core.py
```

### Code Quality

```bash
# Format code
black py_healthcheck tests

# Sort imports
isort py_healthcheck tests

# Lint code
flake8 py_healthcheck tests

# Type checking
mypy py_healthcheck
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for your changes
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a history of changes.

## Support

- 📖 [Documentation](https://py-healthcheck.readthedocs.io)
- 🐛 [Issue Tracker](https://github.com/py-healthcheck/py-healthcheck/issues)
- 💬 [Discussions](https://github.com/py-healthcheck/py-healthcheck/discussions)

## Acknowledgments

- Inspired by the need for comprehensive health checking in microservices
- Built with the Python community's best practices
- Thanks to all contributors and users
