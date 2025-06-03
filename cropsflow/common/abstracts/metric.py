import threading
from abc import abstractmethod, ABC


class Metric(ABC):
    title: str
    description: str

    def __init__(self, title: str, description: str):
        self.title = title
        self.description = description

    @abstractmethod
    def collect(self):
        """Return the current metric value(s)."""
        pass


class GaugeMetric(Metric, ABC):
    def __init__(self, title: str, description: str):
        """
        value_func: function returning current value dynamically
        """
        super().__init__(title, description)
        self._value = 0
        self._lock = threading.Lock()

    def set(self, value):
        with self._lock:
            self._value = value
            return self._value

    def get(self):
        return self._value
