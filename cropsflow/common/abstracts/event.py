"""
Module: event.py

Defines the abstract base class `Event`, a generic dataclass that models
an event with associated metadata and payload.

This module provides a foundational structure for creating event objects
with a consistent interface, including:

- An event name to identify the event type or source.
- A timestamp indicating when the event occurred or was recorded.
- A generic data payload, allowing flexibility for different event content.

The `Event` class is generic over the data type, making it adaptable to
various use cases requiring strongly typed event data.

Usage:
    Subclass `Event` or instantiate it with a specific data type to represent
    concrete events within an application or system.
"""

from abc import ABC
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime
from typing import TypeVar, Generic, Callable, List

D = TypeVar('D')


@dataclass
class EventSubscription:
    data: any = field(default=None)
    target: 'Event' = field(default=None)


EventHandler = Callable[[EventSubscription], None]


class Event(Generic[D], ABC):
    """
    Abstract base class representing a generic event.

    This class provides a structure for events by defining common metadata such as
    the event's name, timestamp, and associated data.

    Type Parameters:
        D: The type of the data associated with the event.

    Attributes:
        id (str): The identifier of the event.
        name (str): The name  of the event.
        description (str): The description of the event.
    """

    def __init__(self, event_id: str, name: str, description: str):
        self.id: str = event_id
        self.name: str = name
        self.description: str = description
        self.__handlers: list[EventHandler] = []

    def add_handler(self, handler: EventHandler) -> 'Event':
        if handler not in self.__handlers:
            self.__handlers.append(handler)
        return self

    def get_handlers(self) -> List[EventHandler]:
        return deepcopy(self.__handlers)

    def handle(self):
        def decorator(func: Callable):
            self.add_handler(func)

        return decorator

    def emit(self, data: any):
        """
        Emit an event to this channel. The event's timestamp is set to the current time.
        All subscribers are notified with the event.
        """
        for handler in self.__handlers:
            handler(data)
