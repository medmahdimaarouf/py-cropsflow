from typing import Generic, TypeVar, Optional, List
from dataclasses import dataclass

T = TypeVar('T')


@dataclass
class ActionOptionMetaData(Generic[T]):
    property: str
    name: str
    required: bool
    default: Optional[T] = None  # Optional to indicate it's not always required
    propertyType: T = None  # Generic type
    select: Optional[List[T]] = None  # Optional list of generic type
