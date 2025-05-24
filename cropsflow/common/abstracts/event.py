from abc import ABC
from datetime import datetime
from typing import TypeVar, Generic

D = TypeVar('D')


class Event(Generic[D], ABC):
    name: str
    date_time: datetime
    data: D
