import datetime
import time
from collections import deque
from typing import List, Callable

from cropsflow.common.abstracts.event import Event

EventSubscriber = Callable[[Event], None]


class EventChannel:
    id: str
    title: str
    description: str
    created_at: float
    owner: str
    __events: deque[Event] = deque()
    __subscribers: List[EventSubscriber] = []

    def __init__(self, id: str, title: str, description: str = ''):
        self.id = id
        self.title = title
        self.description = description
        self.created_at = time.time()

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
