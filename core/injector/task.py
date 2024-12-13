from .container import Container
from common.decorators import TaskDecoratorMetaData
from ..builder.task_template import TaskTemplate


class Task(Container):
    template: TaskTemplate
    metadata: TaskDecoratorMetaData

    def __int__(self, metadata: TaskDecoratorMetaData, host: Container):
        super().__init__(metadata=metadata, host=host)
        self.template = None

    def build(self) -> None:
        pass
