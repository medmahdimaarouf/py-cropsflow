from abc import ABC, abstractmethod


class Logger(ABC):
    @abstractmethod
    def log(self, message: None, *args) -> None:
        pass

    @abstractmethod
    def warning(self, message: None, *args) -> None:
        pass

    @abstractmethod
    def error(self, message: None, *args) -> None:
        pass

    @abstractmethod
    def info(self, message: None, *args) -> None:
        pass

    @abstractmethod
    def debug(self, message: None, *args) -> None:
        pass
