"""
Module: logger.py

Defines the abstract base class `Logger` that specifies a standard interface
for logging functionality across different log levels.

This module provides an extensible framework for implementing custom loggers,
ensuring consistent method signatures for logging general messages, warnings,
errors, informational messages, and debug output.

Classes:
    Logger: Abstract base class declaring methods that must be implemented by
            concrete logger classes to handle various logging levels.

Usage:
    Subclass `Logger` to create specific logging implementations suited to
    different output formats, destinations, or logging frameworks.
"""

from abc import ABC, abstractmethod


class Logger(ABC):
    """
    Abstract base class for logging functionality.

    This interface defines standard logging methods that should be implemented by
    any concrete logger. Each method corresponds to a specific log level.
    """

    @abstractmethod
    def log(self, message: str, *args) -> None:
        """
        Log a general message.

        Args:
            message (str): The message to log.
            *args: Additional arguments to include in the log.
        """

    @abstractmethod
    def warning(self, message: str, *args) -> None:
        """
        Log a warning message.

        Args:
            message (str): The warning message to log.
            *args: Additional arguments to include in the log.
        """

    @abstractmethod
    def error(self, message: str, *args) -> None:
        """
        Log an error message.

        Args:
            message (str): The error message to log.
            *args: Additional arguments to include in the log.
        """

    @abstractmethod
    def info(self, message: str, *args) -> None:
        """
        Log an informational message.

        Args:
            message (str): The informational message to log.
            *args: Additional arguments to include in the log.
        """

    @abstractmethod
    def debug(self, message: str, *args) -> None:
        """
        Log a debug message.

        Args:
            message (str): The debug message to log.
            *args: Additional arguments to include in the log.
        """
