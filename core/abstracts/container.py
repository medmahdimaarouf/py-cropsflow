import uuid
from typing import Any, Dict, Generic, TypeVar
from common.utils import InjectionToken

T = TypeVar('T')


class Container(Generic[T]):
    id: str
    host: "Container"
    instances: Dict[InjectionToken, Any] = {}
    target: T

    def __init__(self, target: T, host: "Container" = None):
        self.id = str(uuid.uuid4())
        self.target = target
        self.host = host
