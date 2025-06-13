from typing import Dict, Any

from cropsflow import C, TaskContext, D
from cropsflow.common import task, pipe, Pipe


@pipe(selector='check-value')
class CheckValuePipe(Pipe):

    def __init__(self):
        super().__init__(data='mock data')

    def accumulate(self, context: TaskContext, options: Dict[str, Any], data: D = None, accessor: str = None) -> None:
        self._data = data


@pipe(selector='mock-value')
class MockValuePipe(Pipe):

    def __init__(self):
        super().__init__(data='mock data')

    def accumulate(self, context: TaskContext, options: Dict[str, Any], data: D = None, accessor: str = None) -> None:
        pass


@task(template_path="./app.task.xml")
class AppTask:
    pass
