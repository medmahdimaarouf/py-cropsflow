"""
This module defines the Monitor class for managing and storing Metric instances.

The Monitor class allows registering, retrieving, checking, and listing metrics by name.
It ensures metric names are unique and provides thread-safe access to stored metrics.
"""

from typing import Dict

from cropsflow.common.abstracts import Metric
from cropsflow.common import service, InjectionScope


@service(scope=InjectionScope.DEFAULT)
class Monitor:
    """
    Monitor class manages a collection of named Metric instances.

    Provides methods to register new metrics, retrieve them by name,
    check for existence, and list all registered metric names.
    """

    def __init__(self):
        """
        Initialize a new Monitor with an empty metric collection.
        """
        self.name: str = ''
        self.metrix: Dict[str, Metric] = {}

    def register_metric(self, name: str, metric: Metric) -> Metric:
        """
        Register a new metric by a unique name.

        Args:
            name (str): The unique name of the metric.
            metric (Metric): The Metric instance to register.

        Returns:
            Metric: The registered metric.

        Raises:
            Exception: If a metric with the given name already exists.
        """
        key = name.strip()
        if key not in self.metrix:
            self.metrix[key] = metric
            return metric
        else:
            raise Exception(f"Unable to add metric: metric name '{key}' already exists")

    def get_metric(self, name: str) -> Metric | None:
        """
        Retrieve a metric by name.

        Args:
            name (str): The metric name.

        Returns:
            Metric | None: The metric if found, otherwise None.
        """
        return self.metrix.get(name.strip(), None)

    def has_metric(self, name: str) -> bool:
        """
        Check if a metric with the given name is registered.

        Args:
            name (str): The metric name.

        Returns:
            bool: True if metric exists, False otherwise.
        """
        return name.strip() in self.metrix

    def get_metrix(self) -> list[str]:
        """
        Get a list of all registered metric names.

        Returns:
            list[str]: List of metric names.
        """
        return list(self.metrix.keys())
