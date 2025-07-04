"""
Module: event_emitter

This module defines the EventEmitter service, which manages multiple EventChannel instances.
It provides methods to create, retrieve, remove, and query event channels by their unique IDs.
"""

from typing import Dict, List

from .event_channel import EventChannel
from cropsflow.common import service, InjectionScope
from .exceptions import DuplicatedChannelException


@service(scope=InjectionScope.DEFAULT)
class EventEmitter:
    """
    Service that manages EventChannel instances.

    Attributes:
        __channels (Dict[str, EventChannel]): Internal dictionary mapping channel IDs to EventChannel instances.
    """

    def __init__(self):
        """
        Initialize an EventEmitter with no channels.
        """
        self.__channels: Dict[str, EventChannel] = {}

    def create_channel(self, name: str, description: str = '') -> EventChannel:
        """
        Create a new EventChannel with the given ID, name, and optional description.

        Args:
            channel_id (str): Unique identifier for the channel.
            name (str): Title of the channel.
            description (str, optional): Description of the channel. Defaults to empty string.

        Returns:
            EventChannel: The newly created event channel.

        Raises:
            Exception: If a channel with the given ID already exists.
        """
        channel = EventChannel()
        setattr(channel, '__id', name.strip().replace(' ', ' ').replace(' ', '-').lower())
        setattr(channel, '__name', name.strip())
        setattr(channel, '__description', description.strip())
        if channel.id not in self.__channels:
            return self.__channels.setdefault(channel.id, channel)
        else:
            raise DuplicatedChannelException(channel.id)

    def get_channels(self) -> List[EventChannel]:
        """
        Retrieve all event channels managed by this emitter.

        Returns:
            List[EventChannel]: List of all event channels.
        """
        return list(self.__channels.values())

    def get_channel(self, channel_id: str) -> EventChannel | None:
        """
        Retrieve a specific event channel by its ID.

        Args:
            channel_id (str): The unique identifier of the channel.

        Returns:
            EventChannel | None: The channel if found, otherwise None.
        """
        return self.__channels.get(channel_id.strip(), None)

    def remove_channel(self, channel_id: str) -> None:
        """
        Remove an event channel by its ID.

        Args:
            channel_id (str): The unique identifier of the channel to remove.

        Raises:
            KeyError: If the channel ID does not exist.
        """
        self.__channels.pop(channel_id.strip())

    def has_channel(self, channel_id: str) -> bool:
        """
        Check if an event channel exists with the given ID.

        Args:
            channel_id (str): The unique identifier of the channel.

        Returns:
            bool: True if channel exists, False otherwise.
        """
        return channel_id.strip() in self.__channels

    def clear(self) -> None:
        """
        Remove all event channels.
        """
        self.__channels.clear()
