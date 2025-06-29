"""
This module defines the Monitor class for managing and storing Metric instances.

The Monitor class allows registering, retrieving, checking, and listing metrics by name.
It ensures metric names are unique and provides thread-safe access to stored metrics.
"""

from typing import Dict, Optional

from cropsflow.common.abstracts import Metric
from scheduler import AsyncScheduler
from scheduler.background_scheduler import BackgroundScheduler


class Monitor:
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
        self.__metrix: Dict[str, Metric] = {}
        self.scheduler: AsyncScheduler = AsyncScheduler()

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
        if metric_id not in self.__metrix:
            setattr(metric, '__name', metric_id)
            setattr(metric, '__description', description)
            setattr(metric, '__id', metric_id)
            self.__metrix.setdefault(metric_id, metric)
            return metric
        else:
            raise Exception(f"Unable to add metric: metric name '{metric_id}' already exists")

    def get_metric(self, name: str) -> Metric | None:
        """
        Retrieve a metric by name.

        Args:
            name (str): The metric name.

        Returns:
            Metric | None: The metric if found, otherwise None.
        """
        return self.__metrix.get(name.strip(), None)

    def has_metric(self, name: str) -> bool:
        """
        Check if a metric with the given name is registered.

        Args:
            name (str): The metric name.

        Returns:
            bool: True if metric exists, False otherwise.
        """
        return name.strip() in self.__metrix

    def get_metrix(self) -> list[str]:
        """
        Get a list of all registered metric names.

        Returns:
            list[str]: List of metric names.
        """
        return list(self.__metrix.keys())

    def start(self):
        pass

    def shutdown(self, wait: bool):
        pass
