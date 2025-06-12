"""
Defines the Option class used to describe a configurable parameter
for an action, including metadata such as type, default value, and description.
"""

from typing import Generic, TypeVar, Optional, List, Type
from dataclasses import dataclass

T = TypeVar('T')


class Option(Generic[T]):
    """
    Describes a configurable option for an action.

    Attributes:
        key (str): Unique key for the option.
        meta_type (Type[T]): The expected type for the option value.
        required (bool): Whether the option is required.
        default (Optional[T]): Default value if not provided.
        select (Optional[List[T]]): A list of allowed values (if any).
        name (str): Display name for the option.
        description (str): Description of the option.
    """

    def __init__(
            self,
            key: str,
            meta_type: Type[T],
            required: bool = False,
            default: Optional[T] = None,
            name: str = '',
            description: str = '',
            select: Optional[List[T]] = None
    ):
        self.key: str = key.strip()
        self.meta_type: Type[T] = meta_type
        self.required: bool = required
        self.default: Optional[T] = default
        self.select: Optional[List[T]] = select
        self.name: str = name.strip()
        self.description: str = description.strip()
