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
from dataclasses import dataclass, field
from datetime import datetime
from typing import TypeVar, Generic

D = TypeVar('D')


@dataclass
class Event(Generic[D], ABC):
    """
    Abstract base class representing a generic event.

    This class provides a structure for events by defining common metadata such as
    the event's name, timestamp, and associated data.

    Type Parameters:
        D: The type of the data associated with the event.

    Attributes:
        name (str): The name or identifier of the event.
        date_time (datetime): The timestamp when the event occurred or was recorded.
        data (D): Payload or metadata associated with the event.
    """

    name: str = field(default_factory=str)
    date_time: datetime = field(default_factory=datetime)
    data: D = field(default=None)
