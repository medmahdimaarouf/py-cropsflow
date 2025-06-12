"""
Module: lifecycle.py

This module defines abstract base classes for lifecycle management interfaces:
`Init` and `Destroy`.

These interfaces are intended to be implemented by classes that require explicit
initialization and cleanup logic. They are useful in dependency-injection systems,
task execution frameworks, or any architecture where controlled resource management
is necessary.

Classes:
    - Init: Defines the `init` method for setup or configuration procedures.
    - Destroy: Defines the `destroy` method for cleanup or teardown procedures.

Usage:
    Implement `Init` when your class needs a configurable initialization step.
    Implement `Destroy` when your class needs to release resources or clean up after execution.
"""

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
