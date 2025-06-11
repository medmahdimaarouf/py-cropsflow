from cropsflow.common.decorators import TaskDecoratorMetaData
from .container import Container


class Task(Container):

    def __init__(self, metadata: TaskDecoratorMetaData, host: Container):
        super().__init__(metadata=metadata, host=host)
