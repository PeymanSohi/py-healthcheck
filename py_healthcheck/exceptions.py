"""
Custom exceptions for py-healthcheck.
"""


class HealthCheckError(Exception):
    """Base exception for health check failures."""
    pass


class ConnectionError(HealthCheckError):
    """Raised when a connection to a service fails."""
    pass


class TimeoutError(HealthCheckError):
    """Raised when a health check times out."""
    pass


class ConfigurationError(HealthCheckError):
    """Raised when there's a configuration issue."""
    pass
