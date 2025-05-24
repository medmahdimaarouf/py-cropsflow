from typing import Dict, List

from .event_channel import EventChannel
from cropsflow.common import service, InjectionScope


@service(scope=InjectionScope.DEFAULT)
class EventEmitter:
    channels: Dict[str, EventChannel] = {}

    def create_channel(self, channel_id: str, title: str, description: str = '') -> EventChannel:
        if channel_id.strip() not in self.channels:
            return self.channels.setdefault(channel_id.strip(), EventChannel(title=title, description=description))
        else:
            raise Exception(f"Channel with id '{channel_id.strip()}' is already existing")

    def get_channels(self) -> List[str]:
        return list(self.channels.keys())

    def get_channel(self, channel_id) -> EventChannel | None:
        return self.channels.get(channel_id.strip(), None)

    def has_channel(self, channel_id: str):
        return channel_id.strip() in self.channels

    def clear(self) -> None:
        self.channels.clear()
