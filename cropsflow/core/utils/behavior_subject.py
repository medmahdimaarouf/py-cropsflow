from typing import Callable, List, Any, TypeVar, Generic

T = TypeVar('T')


class BehaviorSubject(Generic[T]):
    def __init__(self, initial_value: T):
        self._value = initial_value
        self._subscribers: List[Callable[[T], None]] = []

    def subscribe(self, callback: Callable[[T], None]):
        # Immediately emit current value to the new subscriber
        callback(self._value)
        self._subscribers.append(callback)

    def next(self, value: T):
        self._value = value
        for callback in self._subscribers:
            callback(value)

    @property
    def value(self) -> T:
        return self._value
