"""
Abstract base class for asynchronous builders with generic return type.
"""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic

B = TypeVar('B')


class Builder(Generic[B], ABC):
    """
    Generic abstract base class representing a builder
    that asynchronously builds and returns an instance of type B.
    """

    @abstractmethod
    async def build(self) -> B:
        """
        Asynchronously build and return an instance of type B.

        Returns:
            B: The built instance.
        """
