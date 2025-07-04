"""
This module defines the Monitor class for managing and storing Metric instances.

The Monitor class allows registering, retrieving, checking, and listing metrics by name.
It ensures metric names are unique and provides thread-safe access to stored metrics.
"""
import threading
from typing import Optional, Callable, Dict

from cropsflow.common.abstracts import Metric
from cropsflow.scheduler import AsyncScheduler
from .metric_watcher import MetricWatcher


class Monitor(AsyncScheduler):
    """
    Monitor class manages a collection of named Metric instances.

    Provides methods to register new metrics, retrieve them by name,
    check for existence, and list all registered metric names.
    """

    @property
    def name(self) -> Optional[str]:
        return getattr(self, '__name', None)

    @property
    def description(self) -> Optional[str]:
        return getattr(self, '__description')

    @property
    def id(self) -> Optional[str]:
        return getattr(self, '__id')

    def __init__(self):
        """
        Initialize a new Monitor with an empty metric collection.
        """
        super().__init__()
        self.scheduler: AsyncScheduler = AsyncScheduler()
        self.__watchers: Dict[str, MetricWatcher] = {}

    def register_metric(self, name: str, metric: Metric, description: str = None,
                        ms_time_interval: int = 1) -> Metric:
        """
        Register a new metric by a unique name.
        """
        metric_id = name.strip().lower().replace('  ', ' ').replace(' ', '-')
        if metric_id not in self.__watchers:
            setattr(metric, '__name', name)
            setattr(metric, '__description', description)
            setattr(metric, '__id', metric_id)
            watcher: MetricWatcher = MetricWatcher(metric=metric, ms_time_interval=ms_time_interval)
            self.__watchers.setdefault(metric_id, watcher)
            self.schedule_every(seconds=ms_time_interval, call_back=watcher.notify)  # collect should be wrapped
            return metric
        else:
            raise Exception(f"Unable to add metric: metric name '{metric_id}' already exists")

    def get_metric(self, metric_id: str) -> Metric | None:
        """
        Retrieve a metric by name.

        Args:
            metric_id (str): The metric id.

        Returns:
            Metric | None: The metric if found, otherwise None.
        """
        watcher = self.__watchers.get(metric_id.strip(), None)
        return None if watcher is None else watcher.metric

    def has_metric(self, metric_id: str) -> bool:
        """
        Check if a metric with the given name is registered.

        Args:
            metric_id (str): The metric id.

        Returns:
            bool: True if metric exists, False otherwise.
        """
        return metric_id.strip() in self.__watchers

    def get_metrics(self) -> list[str]:
        """
        Get a list of all registered metric names.

        Returns:
            list[str]: List of metric names.
        """
        return list(self.__watchers.keys())

    def watch(self, metric_id: str, callback: [[str, any], None]):
        watcher: MetricWatcher = self.__watchers.get(metric_id.strip(), None)
        if watcher is not None:
            watcher.subscribe(callback)

    def unwatch(self, metric_id: str, callback: [[str, any], None]):
        if metric_id is None:
            raise ValueError('Unwatch metric id is none')
        watcher: MetricWatcher = self.__watchers.get(metric_id.strip(), None)
        if watcher is not None:
            watcher.unsubscribe(callback)
        else:
            raise ValueError(f'Watcher with metric {metric_id} is not found')

    def watch_all(self, callback: [[str, any], None]):
        for watcher in self.__watchers.values():
            watcher.subscribe(callback)

    def unwatch_all(self, metric_id: str = None, callback: Callable = None):
        if metric_id is not None:
            watcher: MetricWatcher = self.__watchers.get(metric_id.strip(), None)
            if watcher is not None:
                if callback is None:
                    watcher.clear()
                else:
                    watcher.unsubscribe(callback)
        else:
            for watcher in self.__watchers.values():
                if callback is None:
                    watcher.clear()
                else:
                    watcher.unsubscribe(callback)
