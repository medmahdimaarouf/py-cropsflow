"""
Module: monitor.py

Defines the Monitor class responsible for managing and tracking named metrics.

The Monitor class provides functionality to register, retrieve, and check
metrics identified by unique string names. It acts as a container for multiple
Metric instances, allowing centralized access and management.

Classes:
    Monitor: Manages a collection of named Metric instances, ensuring uniqueness and
             providing query and retrieval capabilities.
"""

from typing import Dict
from .metric import Metric


class Monitor:
    """
    A class for monitoring and managing named metrics.

    Attributes:
        name (str): The name of the monitor instance.
        metrix (Dict[str, Metric]): A dictionary mapping metric names to Metric instances.
    """

    def __init__(self, name: str):
        """
        Initialize a Monitor with a given name.

        Args:
            name (str): The name of the monitor instance.
        """
        self.name: str = name
        self.metrix: Dict[str, Metric] = {}

    def register_metric(self, name: str, metric: Metric) -> Metric:
        """
        Register a new metric under the given name.

        Args:
            name (str): The name to register the metric under.
            metric (Metric): The Metric instance to register.

        Returns:
            Metric: The registered metric instance.

        Raises:
            Exception: If a metric with the same name already exists.
        """
        key = name.strip()
        if key not in self.metrix:
            self.metrix[key] = metric
            return metric
        raise ValueError(f"Unable to add metric: metric name '{key}' already exists")

    def get_metric(self, name: str) -> Metric | None:
        """
        Retrieve a registered metric by name.

        Args:
            name (str): The name of the metric.

        Returns:
            Metric | None: The corresponding metric, or None if not found.
        """
        return self.metrix.get(name.strip(), None)

    def has_metric(self, name: str) -> bool:
        """
        Check if a metric with the given name is registered.

        Args:
            name (str): The name of the metric.

        Returns:
            bool: True if the metric exists, False otherwise.
        """
        return name.strip() in self.metrix

    def get_metrix(self) -> list[str]:
        """
        Get a list of all registered metric names.

        Returns:
            list[str]: List of metric names.
        """
        return list(self.metrix.keys())
