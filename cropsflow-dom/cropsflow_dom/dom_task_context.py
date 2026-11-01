from dataclasses import dataclass
from typing import TypeVar, Generic

E = TypeVar('E')


@dataclass
class DOMTaskContext(Generic[E]):
    element: E = None

    def __init__(self, element: E):
        self.element = element
