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

