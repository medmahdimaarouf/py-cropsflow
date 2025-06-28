"""
Module: event_channel

This module defines the EventChannel class, which manages a stream of events,
subscribers, and event emission notifications. It allows subscribing to events,
storing emitted events, and notifying all subscribers when new events occur.

The EventChannel tracks metadata such as channel ID, name, description, creation time,
and the owner of the channel.
"""

import datetime
import time
from collections import deque
from copy import deepcopy
from typing import List, Callable, Optional

from cropsflow.common.abstracts.event import Event


class EventChannel:
    """
    Represents an event channel that holds events and notifies subscribers when new events are emitted.

    Attributes:
        id (str): Unique identifier for the channel.
        name (str): Human-readable name of the channel.
        description (str): Optional description of the channel.
        created_at (float): Timestamp of channel creation (epoch seconds).
        owner (str): Username of the owner of the channel.
    """

    def __init__(self, channel_id: str, name: str, description: str = ''):
        """
        Initialize a new EventChannel instance.

        Args:
            channel_id (str): Unique identifier for the channel.
            name (str): name of the channel.
            description (str, optional): Description of the channel. Defaults to an empty string.
        """
        self.id: str = channel_id
        self.name: str = name
        self.description: str = description
        self.created_at: float = time.time()
        self.__events: dict[str, Event] = {}

    def clear(self):
        """
        Clear all stored events from the channel.
        """
        self.__events.clear()

    def events(self) -> list[Event]:
        """
        Get a list of all events currently stored in the channel.

        Returns:
            List[Event]: List of stored events in order of emission.
        """
        return deepcopy(list(self.__events.values()))

    def event(self, event_id: str) -> Optional[Event]:
        return self.__events.get(event_id, None)

    def register(self, event: Event) -> Event:
        return self.__events.setdefault(event.id, event)
