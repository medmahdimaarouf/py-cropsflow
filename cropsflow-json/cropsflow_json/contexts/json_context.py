from dataclasses import dataclass

from cropsflow import TaskContext


@dataclass()
class JSONContext(TaskContext):
    data: None

    def __int__(self, data: None):
        self.data = data
