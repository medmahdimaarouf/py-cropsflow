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
    """

    @property
    def id(self) -> str:
        return self.__name.strip().replace(' ', ' ').replace(' ', '-').lower()

    @property
    def name(self) -> str:
        return self.__name.strip()

    @property
    def description(self) -> str:
        self.description or ''

    def __init__(self, name: str, description: str = ''):
        """
        Initialize a new EventChannel instance.

        Args:
            name (str): name of the channel.
            description (str, optional): Description of the channel. Defaults to an empty string.
        """
        self.__name: str = name
        self.__description: str = description
        self.__created_at: float = time.time()
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
