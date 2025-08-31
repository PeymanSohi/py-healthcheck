# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of py-healthcheck
- Core health check functionality with async/sync support
- Built-in checks for PostgreSQL, MySQL, Redis, MongoDB, Elasticsearch, HTTP
- Framework integrations for Flask, FastAPI, and Django
- CLI tool with rich output support
- Comprehensive test suite
- Full type hints and documentation

### Changed
- Nothing yet

### Deprecated
- Nothing yet

### Removed
- Nothing yet

### Fixed
- Nothing yet

### Security
- Nothing yet

## [0.1.0] - 2024-01-XX

### Added
- Initial release
- Core health check registry and execution engine
- Support for both synchronous and asynchronous health checks
- Built-in health checks for common services:
  - PostgreSQL (with psycopg2 and asyncpg support)
  - MySQL (with pymysql and aiomysql support)
  - Redis (with redis and aioredis support)
  - MongoDB (with pymongo and motor support)
  - Elasticsearch (with elasticsearch-py support)
  - HTTP endpoints (with requests and httpx support)
- Framework integrations:
  - Flask: `register_health_endpoint()` function
  - FastAPI: `get_health_router()` function
  - Django: `healthcheck_view()` function
- CLI tool with the following features:
  - Support for all built-in check types
  - JSON and table output formats
  - Configurable timeouts
  - Verbose and quiet modes
  - Rich table output (optional)
- Custom health check support via decorators and programmatic registration
- Comprehensive error handling with specific exception types
- Parallel execution of health checks for better performance
- Detailed output with timing information and error details
- Full type hints throughout the codebase
- Comprehensive test suite with >90% coverage
- PyPI-ready packaging with proper metadata
- MIT license

### Technical Details
- Python 3.8+ support
- Async/await support with asyncio
- Type hints with mypy compatibility
- Black code formatting
- Comprehensive documentation
- CI/CD ready with GitHub Actions
- Pre-commit hooks for code quality

### Dependencies
- Core: click, httpx
- Optional database drivers: psycopg2-binary, asyncpg, pymysql, aiomysql, redis, aioredis, pymongo, motor, elasticsearch
- Optional framework support: flask, fastapi, django
- Optional CLI enhancements: rich
- Development: pytest, black, isort, flake8, mypy, pre-commit
