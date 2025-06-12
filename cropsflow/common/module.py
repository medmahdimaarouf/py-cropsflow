"""
Module: common_module.py

Defines the `CommonModule` class, which acts as a container module aggregating a set of common
actions and data transformation pipes for use within the application framework.

This module utilizes the `@module` decorator to declare and export frequently used components
such as actions and pipes. The module system allows for organized dependency injection,
component reuse, and streamlined application composition.

Components included:

Actions:
    - DelayAction: Introduces delays in task execution.
    - IterateAction: Facilitates iteration over collections.
    - CMDAction: Executes shell or system commands.

Pipes:
    - MapPipe: Transforms dictionary-like data structures.
    - ListPipe: Processes list-type data.
    - IntegerPipe: Converts or validates integer values.
    - TextPipe: Handles string transformations or validations.
    - DecimalPipe: Processes decimal numbers for parsing or formatting.

The `CommonModule` declares these components and exports them for accessibility in other
modules or parts of the system.

Usage:
    Import the `CommonModule` where these actions and pipes are needed to benefit from
    centralized declarations and exports.

Example:
    from common_module import CommonModule
"""

from .actions import DelayAction, IterateAction, CMDAction
from .decorators.module import module
from .pipes import MapPipe, ListPipe, IntegerPipe, TextPipe, DecimalPipe


@module(
    declarations=[
        DelayAction,
        IterateAction,
        CMDAction,
        MapPipe,
        ListPipe,
        IntegerPipe,
        TextPipe,
        DecimalPipe
    ],
    exports=[
        DelayAction,
        IterateAction,
        CMDAction,
        MapPipe,
        ListPipe,
        IntegerPipe,
        TextPipe,
        DecimalPipe
    ]
)
class CommonModule:
    """
    A module that bundles common actions and pipes.

    This class is a container for reusable components that are widely used across
    different parts of the application. It serves as a centralized place to declare
    and export these components for dependency injection.

    Attributes:
        None (This class only serves as a declaration container.)
    """
