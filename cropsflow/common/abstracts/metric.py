from abc import abstractmethod, ABC


class Metric(ABC):
    title: str
    description: str

    def __init__(self, title: str, description: str = ""):
        self.title = title
        self.description = description

    @abstractmethod
    def collect(self):
        """Return the current metric value(s)."""
        pass
