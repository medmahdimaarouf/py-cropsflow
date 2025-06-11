from abc import ABC, abstractmethod


class Init(ABC):
    """
    Interface for initialization behavior.

    Classes that inherit from Init should implement the `init` method to perform
    setup operations such as allocating resources, setting initial state, or configuring dependencies.
    """

    @abstractmethod
    def init(self, **args) -> None:
        """
        Perform initialization logic.

        Args:
            **args: Arbitrary keyword arguments for initialization configuration.
        """
        pass


class Destroy(ABC):
    """
    Interface for destruction or cleanup behavior.

    Classes that inherit from Destroy should implement the `destroy` method to perform
    cleanup operations such as releasing resources, closing connections, or saving state.
    """

    @abstractmethod
    def destroy(self, **args) -> None:
        """
        Perform cleanup or destruction logic.

        Args:
            **args: Arbitrary keyword arguments for destruction configuration.
        """
        pass
