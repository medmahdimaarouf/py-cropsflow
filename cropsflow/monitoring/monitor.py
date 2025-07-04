"""
This module defines the Monitor class for managing and storing Metric instances.

The Monitor class allows registering, retrieving, checking, and listing metrics by name.
It ensures metric names are unique and provides thread-safe access to stored metrics.
"""

from typing import Dict, Optional, Callable

from cropsflow.common.abstracts import Metric
from cropsflow.scheduler import AsyncScheduler


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
        self.__metrics: Dict[str, Metric] = {}
        self.scheduler: AsyncScheduler = AsyncScheduler()
        self.__watchers: list[Callable[[str, any], None]] = []

    def register_metric(self, name: str, metric: Metric, description: str = None) -> Metric:
        """
        Register a new metric by a unique name.

        Args:
            name (str): The unique name of the metric.
            metric (Metric): The Metric instance to register.

        Returns:
            Metric: The registered metric.

        Raises:
            Exception: If a metric with the given name already exists.
            :param name: metric name
            :param metric: metric instance
            :param description: metric description
        """
        metric_id = name.strip().lower().replace('  ', ' ').replace(' ', '-')
        if metric_id not in self.__metrics:
            setattr(metric, '__name', name)
            setattr(metric, '__description', description)
            setattr(metric, '__id', metric_id)
            self.__metrics.setdefault(metric_id, metric)
            self.schedule_every(seconds=1000, call_back=metric.collect)  # collect should be wrapped
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
        return self.__metrics.get(metric_id.strip(), None)

    def has_metric(self, metric_id: str) -> bool:
        """
        Check if a metric with the given name is registered.

        Args:
            metric_id (str): The metric id.

        Returns:
            bool: True if metric exists, False otherwise.
        """
        return metric_id.strip() in self.__metrics

    def get_metrics(self) -> list[str]:
        """
        Get a list of all registered metric names.

        Returns:
            list[str]: List of metric names.
        """
        return list(self.__metrics.keys())
