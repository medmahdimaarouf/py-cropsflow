import datetime
import time
from collections import deque
from getpass import getpass
from typing import List, Callable

from cropsflow.common.abstracts.event import Event

EventSubscriber = Callable[[Event], None]


class EventChannel:

    def __init__(self, channel_id: str, title: str, description: str = ''):
        self.id: str = channel_id
        self.title: str = title
        self.description: str = description
        self.created_at: float = time.time()
        self.__events: deque[Event] = deque()
        self.__subscribers: List[EventSubscriber] = []
        self.owner: str = getpass.getuser()

    def clear_events(self):
        self.__events.clear()

    def events(self) -> list[Event]:
        return list(self.__events)

    def clear_subscribers(self):
        self.__subscribers.clear()

    def subscribe(self, subscriber: EventSubscriber):
        if subscriber is not None:
            self.__subscribers.append(subscriber)

    def unsubscribe(self, subscriber: EventSubscriber):
        return self.__subscribers.remove(subscriber)

    def emit(self, event: Event):
        if event is not None:
            event.date_time = datetime.datetime().now()
            self.__events.append(event)
            for subscriber in self.__subscribers:
                subscriber(event)
