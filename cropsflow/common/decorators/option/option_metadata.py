from typing import Generic, TypeVar, Optional, List, Type
from dataclasses import dataclass, field

T = TypeVar('T')


@dataclass
class Option(Generic[T]):
    key: str = field(default_factory=str)
    default: T = None  # Optional to indicate it's not always required
    meta_type: Type[T] = None  # Generic type
    select: List[T] = None  # Optional list of generic type
    name: str = ''
    description: str = ''
    required: bool = False

    def __init__(self, key: str, meta_type: Type[T], required: bool = False, default: T = None, name: str = '',
                description: str = '', select: List[T] = None):
        self.key = key.strip()
        self.meta_type = meta_type
        self.default = default
        self.required = required
        self.select = select
        self.name = name.strip()
        self.description = description.strip()
