import asyncio
import threading
from datetime import time
from typing import Callable, final, List

from cropsflow.common.abstracts import Metric


@final
class MetricWatcher:
    __slots__ = ('metric', 'subscriptions', 'ms_time_interval', '__lock')

    def __init__(self, metric: Metric, ms_time_interval: int):
        self.metric: Metric = metric
        self.ms_time_interval: int = ms_time_interval
        self.subscriptions: List[Callable[[str, any], any]] = []
        self.__lock: threading.Lock = threading.Lock()

    def subscribe(self, subscription: Callable[[str, any], any]) -> None:
        with self.__lock:
            self.subscriptions.append(subscription)

    def unsubscribe(self, subscription: Callable[[str, any], any]) -> None:
        with self.__lock:
            self.subscriptions.remove(subscription)

    async def notify(self):
        value: any = self.metric.collect()
        if len(self.subscriptions):
            with self.__lock:
                for subscribe in self.subscriptions:
                    await subscribe(self.metric.id, value)

    def clear(self):
        with self.__lock:
            self.subscriptions.clear()
