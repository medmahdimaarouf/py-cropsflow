from enum import Enum


class ResolveStatus(Enum):
    NONE = 0
    PENDING = 1
    RESOLVED = 2
    ERROR = 3
