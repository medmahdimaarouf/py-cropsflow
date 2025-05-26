import queue
from collections import deque
from .worker import Worker


class WorkersQueue:
    __queue: deque = deque()

    @property
    def workers_list(self) -> list[Worker]:
        return list(self.__queue)

    def pop(self) -> Worker:
        return self.__queue.pop()

    def append(self, worker: Worker):
        self.__queue.append(worker)

    def reverse(self) -> None:
        self.__queue.reverse()
