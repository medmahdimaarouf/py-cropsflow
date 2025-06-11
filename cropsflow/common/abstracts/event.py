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
