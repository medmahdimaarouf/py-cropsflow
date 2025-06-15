from typing import Dict, Any

from cropsflow import TaskContext
from cropsflow.common import task, pipe, Pipe


@pipe(selector='check-value')
class CheckValuePipe(Pipe):

    def __init__(self):
        super().__init__(data='mock data')

    def transform(self, data: any = None, options: Dict[str, Any] = None) -> None:
        self._data = data


@pipe(selector='mock-value')
class MockValuePipe(Pipe):

    def __init__(self):
        super().__init__(data='mock data')

    def transform(self, data: any = None, options: Dict[str, Any] = None) -> None:
        pass


@task(template_path="./app.task.xml")
class AppTask:
    pass
