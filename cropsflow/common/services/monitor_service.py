"""
Monitor service definition.
"""

from ..decorators import service, InjectionScope


@service(scope=InjectionScope.DEFAULT)
class Monitor:
    """A basic monitoring service."""
