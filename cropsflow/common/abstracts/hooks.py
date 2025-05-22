from abc import ABC, abstractmethod


class Init(ABC):
    @abstractmethod
    def init(self, **args) -> None:
        pass


class Destroy(ABC):
    @abstractmethod
    def destroy(self, **args) -> None:
        pass
