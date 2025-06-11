import threading
from abc import ABC, abstractmethod


class Metric(ABC):
    """
    Abstract base class for a generic metric.

    Attributes:
        title (str): The human-readable name of the metric.
        description (str): A brief explanation of what the metric represents.
    """

    title: str
    description: str

    def __init__(self, title: str, description: str):
        """
        Initialize the metric with a title and description.

        Args:
            title (str): The name of the metric.
            description (str): A brief description of the metric.
        """
        self.title = title
        self.description = description

    @abstractmethod
    def collect(self):
        """
        Collect the current value(s) of the metric.

        This method must be implemented by subclasses.

        Returns:
            Any: The current metric value(s).
        """
        pass


class GaugeMetric(Metric, ABC):
    """
    A metric that represents a single numerical value which can be set directly.

    This class provides thread-safe methods to set and retrieve the current value.

    Attributes:
        _value (int | float): The current value of the metric.
        _lock (threading.Lock): A lock to ensure thread-safe access to the value.
    """

    def __init__(self, title: str, description: str):
        """
        Initialize the gauge metric with a title, description, and default value.

        Args:
            title (str): The name of the metric.
            description (str): A brief description of the metric.
        """
        super().__init__(title, description)
        self._value = 0
        self._lock = threading.Lock()

    def set(self, value):
        """
        Set the current value of the gauge.

        Args:
            value (int | float): The new value to assign.

        Returns:
            int | float: The value that was set.
        """
        with self._lock:
            self._value = value
            return self._value

    def get(self):
        """
        Retrieve the current value of the gauge.

        Returns:
            int | float: The current metric value.
        """
        return self._value
