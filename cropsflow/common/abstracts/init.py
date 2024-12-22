from abc import ABC, abstractmethod


class Init(ABC):
    @abstractmethod
    def init(self, **args) -> None:
        pass
