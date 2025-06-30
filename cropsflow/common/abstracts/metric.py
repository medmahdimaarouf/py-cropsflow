"""
Module: metrics.py

Defines abstract and concrete classes for metric collection and representation.

This module provides a flexible framework for defining metrics, including
an abstract base class `Metric` for general metrics and a `GaugeMetric`
subclass representing a thread-safe, settable numerical metric.

Classes:
    Metric: Abstract base class requiring implementation of a metric collection method.
    GaugeMetric: Thread-safe metric holding a single numerical value that can be set and retrieved.

Usage:
    Extend `Metric` to implement specific metric types.
    Use `GaugeMetric` for metrics representing numerical values that may be updated concurrently.
"""
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import time
from typing import TypeVar, Generic, Optional

V = TypeVar('V')


class Metric(Generic[V], ABC):
    """
    Abstract base class for a generic metric.
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

    @property
    def value(self) -> V:
        return self.__value

    def __init__(self, initial: V):
        """
        Initialize the metric with a title and description.
        """
        self.__value: V = initial

    @abstractmethod
    def collect(self) -> V:
        """
        Collect the current value(s) of the metric.

        This method must be implemented by subclasses.

        Returns:
            Any: The current metric value(s).
        """


class GaugeMetric(Metric[float], ABC):
    """
    A metric that represents a single numerical value which can be set directly.

    This class provides thread-safe methods to set and retrieve the current value.

    """

    def __init__(self, max_value: int, min_value: int = 0):
        """
        Initialize the gauge metric with a title, description, and default value.

        Args:
            name (str): The name of the metric.
            description (str): A brief description of the metric.
            max_value (int): The max gauge value of the metric.
            min_value (int): The min gauge value of the metric.
        """
        super().__init__(initial=min_value)
        self.max: int = max_value
        self.min: int = min_value

    def set_max(self, max_value: int):
        self.max = max_value

    def set_min(self, min_value: int):
        self.min = min_value


class IndicatorMetric(Metric[float], ABC):
    def __init__(self, initial: float = 0, amount: float = None):
        """
        Initialize the gauge metric with a title, description, and default value.
        """
        super().__init__(initial=initial)
        self.amount: float = amount


class SerialMetric(Metric[dict], ABC):
    @dataclass
    class SerialMetricLegend:
        pass

    def __init__(self, name: str, description: str, initial: dict, amount: float = None):
        super().__init__(name=name, description=description, initial=initial)
        self.amount: float = amount


class CounterMetric(Metric):
    """
    Thread-safe counter metric.

    Allows incrementing a count safely across threads.
    """

    def __init__(self):
        """
        Initialize a new Counter metric.

        Args:
            name (str): Name of the metric.
            description (str, optional): Optional description.
        """
        super().__init__(initial=0)

    def increment(self, amount=1):
        """
        Increment the counter by a specified amount.

        Args:
            amount (int): Amount to increment by, defaults to 1.
        """
        self._value += amount

    def collect(self):
        """
        Get the current count value.

        Returns:
            int: Current count.
        """
        return self._value


class HistogramMetric(Metric):
    """
    Histogram metric buckets observed values and counts occurrences.

    Useful for distribution analysis over predefined bucket ranges.
    """

    def __init__(self, name, buckets=None, description=""):
        """
        Initialize Histogram with optional bucket boundaries.

        Args:
            name (str): Metric name.
            buckets (list, optional): List of bucket upper bounds. Defaults to common ranges.
            description (str, optional): Optional description.
        """
        super().__init__(name, description)
        if buckets is None:
            buckets = [0.1, 0.5, 1, 5, 10, float("inf")]
        self.buckets = sorted(buckets)
        self.counts = defaultdict(int)
        self._lock = threading.Lock()

    def observe(self, value):
        """
        Observe a value and increment the appropriate bucket count.

        Args:
            value (float): Observed value.
        """
        with self._lock:
            for bucket in self.buckets:
                if value <= bucket:
                    self.counts[bucket] += 1
                    break

    def collect(self):
        """
        Return counts per bucket.

        Returns:
            dict: Mapping of bucket upper bounds to counts.
        """
        with self._lock:
            return dict(self.counts)
