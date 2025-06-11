from typing import Dict, List

from .event_channel import EventChannel
from cropsflow.common import service, InjectionScope


@service(scope=InjectionScope.DEFAULT)
class EventEmitter:

    def __init__(self):
        self.__channels: Dict[str, EventChannel] = {}

    def create_channel(self, channel_id: str, title: str, description: str = '') -> EventChannel:
        if channel_id.strip() not in self.__channels:
            return self.__channels.setdefault(channel_id.strip(),
                                              EventChannel(id=channel_id.strip(), title=title, description=description))
        else:
            raise Exception(f"Channel with id '{channel_id.strip()}' is already existing")

    def get_channels(self) -> list[EventChannel]:
        return self.__channels.values()

    def get_channel(self, channel_id: str) -> EventChannel | None:
        return self.__channels.get(channel_id.strip(), None)

    def remove_channel(self, channel_id: str) -> None:
        self.__channels.pop(channel_id)

    def has_channel(self, channel_id: str):
        return channel_id.strip() in self.__channels

    def clear(self) -> None:
        self.__channels.clear()
