"""
This module provides thread-safe metric classes for monitoring application performance
and behavior. It includes implementations for counters, timers, histograms, summaries,
and binary indicators. These metrics can be used to collect quantitative data about
events, durations, distributions, and state flags.

Classes:
    Counter: A simple incrementing counter.
    Timer: Records durations and counts events, with a context manager for timing.
    Histogram: Buckets observed values into ranges and counts occurrences.
    Summary: Stores observed values and calculates statistical summaries.
    Info: Stores static informational key-value pairs.
    BinaryIndicator: Represents a boolean state that can be queried and represented as int or string.
"""

import threading
import time
from abc import ABC
from collections import defaultdict

from cropsflow.common.abstracts import Metric


class Counter(Metric):
    """
    Thread-safe counter metric.

    Allows incrementing a count safely across threads.
    """

    def __init__(self, name, description=""):
        """
        Initialize a new Counter metric.

        Args:
            name (str): Name of the metric.
            description (str, optional): Optional description.
        """
        super().__init__(name, description)
        self._value = 0
        self._lock = threading.Lock()

    def increment(self, amount=1):
        """
        Increment the counter by a specified amount.

        Args:
            amount (int): Amount to increment by, defaults to 1.
        """
        with self._lock:
            self._value += amount

    def collect(self):
        """
        Get the current count value.

        Returns:
            int: Current count.
        """
        with self._lock:
            return self._value


class Timer(Metric):
    """
    Records durations and counts of timed events.

    Provides a context manager to measure elapsed time of code blocks.
    """

    def __init__(self, name, description=""):
        """
        Initialize a Timer metric.

        Args:
            name (str): Name of the metric.
            description (str, optional): Optional description.
        """
        super().__init__(name, description)
        self._count = 0
        self._total_time = 0.0
        self._lock = threading.Lock()

    def record(self, duration_seconds: float):
        """
        Record a duration in seconds.

        Args:
            duration_seconds (float): Duration to add.
        """
        with self._lock:
            self._count += 1
            self._total_time += duration_seconds

    def time(self):
        """
        Context manager to time a block of code.

        Usage:
            with timer.time():
                # code to time

        Returns:
            TimerContext: Context manager instance.
        """

        class TimerContext:
            def __init__(self, timer):
                self.timer = timer

            def __enter__(self):
                self.start = time.perf_counter()
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                end = time.perf_counter()
                self.timer.record(end - self.start)

        return TimerContext(self)

    def collect(self):
        """
        Return collected timing data.

        Returns:
            dict: Dictionary with keys "count", "total_time", "avg_time".
        """
        with self._lock:
            avg = self._total_time / self._count if self._count else 0
            return {"count": self._count, "total_time": self._total_time, "avg_time": avg}


class Histogram(Metric):
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


class Summary(Metric):
    """
    Summary metric stores observed values and calculates quantiles and averages.
    """

    def __init__(self, name, description=""):
        """
        Initialize Summary metric.

        Args:
            name (str): Metric name.
            description (str, optional): Optional description.
        """
        super().__init__(name, description)
        self.values = []
        self._lock = threading.Lock()

    def observe(self, value):
        """
        Record an observed value.

        Args:
            value (float): Value to record.
        """
        with self._lock:
            self.values.append(value)

    def collect(self):
        """
        Return statistics on observed values.

        Returns:
            dict: Contains count, min, max, percentiles, and average.
        """
        with self._lock:
            count = len(self.values)
            if count == 0:
                return {}
            sorted_vals = sorted(self.values)

            def percentile(p):
                k = int(p * count)
                return sorted_vals[min(k, count - 1)]

            return {
                "count": count,
                "min": sorted_vals[0],
                "max": sorted_vals[-1],
                "p50": percentile(0.50),
                "p90": percentile(0.90),
                "p99": percentile(0.99),
                "avg": sum(self.values) / count
            }


class Info(Metric):
    """
    Info metric stores static informational key-value pairs.
    """

    def __init__(self, name, info: dict, description=""):
        """
        Initialize Info metric.

        Args:
            name (str): Metric name.
            info (dict): Dictionary of info values.
            description (str, optional): Optional description.
        """
        super().__init__(name, description)
        self.info = info

    def collect(self):
        """
        Return stored info dictionary.

        Returns:
            dict: Information dictionary.
        """
        return self.info


class BinaryIndicator:
    """
    Represents a binary (boolean) state indicator.

    Provides methods to set, get, and represent the state.
    """

    def __init__(self, name: str, description: str = ""):
        """
        Initialize a BinaryIndicator.

        Args:
            name (str): Name of the indicator.
            description (str, optional): Description.
        """
        self.name = name
        self.description = description
        self.state = False

    def set(self, value: bool):
        """
        Set the indicator state.

        Args:
            value (bool): State value.
        """
        self.state = value

    def get(self) -> bool:
        """
        Get the indicator state.

        Returns:
            bool: Current state.
        """
        return self.state

    def as_int(self) -> int:
        """
        Get the indicator state as int (1 or 0).

        Returns:
            int: 1 if True, else 0.
        """
        return 1 if self.state else 0

    def __str__(self):
        """
        String representation of the indicator state.

        Returns:
            str: Name and state ("Yes" or "No").
        """
        return f"{self.name}: {'Yes' if self.state else 'No'}"
