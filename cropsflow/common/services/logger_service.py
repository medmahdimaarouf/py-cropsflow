"""
Logger service implementation.
"""

from ..decorators import service, InjectionScope


@service(scope=InjectionScope.DEFAULT)
class Logger:
    """A simple logger service."""
