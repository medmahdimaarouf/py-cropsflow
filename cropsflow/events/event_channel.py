"""
Module: event_channel

This module defines the EventChannel class, which manages a stream of events,
subscribers, and event emission notifications. It allows subscribing to events,
storing emitted events, and notifying all subscribers when new events occur.

The EventChannel tracks metadata such as channel ID, title, description, creation time,
and the owner of the channel.
"""

import datetime
import time
from collections import deque
from typing import List, Callable

from cropsflow.common.abstracts.event import Event

EventSubscriber = Callable[[Event], None]


class EventChannel:
    """
    Represents an event channel that holds events and notifies subscribers when new events are emitted.

    Attributes:
        id (str): Unique identifier for the channel.
        title (str): Human-readable title of the channel.
        description (str): Optional description of the channel.
        created_at (float): Timestamp of channel creation (epoch seconds).
        owner (str): Username of the owner of the channel.
    """

    def __init__(self, channel_id: str, title: str, description: str = ''):
        """
        Initialize a new EventChannel instance.

        Args:
            channel_id (str): Unique identifier for the channel.
            title (str): Title of the channel.
            description (str, optional): Description of the channel. Defaults to an empty string.
        """
        self.id: str = channel_id
        self.title: str = title
        self.description: str = description
        self.created_at: float = time.time()
        self.__events: deque[Event] = deque()
        self.__subscribers: List[EventSubscriber] = []

    def clear_events(self):
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
        return list(self.__events)

    def clear_subscribers(self):
        """
        Remove all subscribers from the channel.
        """
        self.__subscribers.clear()

    def subscribe(self, subscriber: EventSubscriber):
        """
        Add a new subscriber to receive events emitted by this channel.

        Args:
            subscriber (EventSubscriber): Callable that accepts an Event parameter.
        """
        if subscriber is not None:
            self.__subscribers.append(subscriber)

    def unsubscribe(self, subscriber: EventSubscriber):
        """
        Remove a subscriber from the channel.

        Args:
            subscriber (EventSubscriber): The subscriber to remove.

        Raises:
            ValueError: If the subscriber is not found in the subscribers list.
        """
        return self.__subscribers.remove(subscriber)

    def emit(self, event: Event):
        """
        Emit an event to this channel. The event's timestamp is set to the current time.
        All subscribers are notified with the event.

        Args:
            event (Event): The event to emit.
        """
        if event is not None:
            event.date_time = datetime.datetime.now()
            self.__events.append(event)
            for subscriber in self.__subscribers:
                subscriber(event)
