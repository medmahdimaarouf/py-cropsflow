from common.schemas import DecoratorMetaData


class TaskDecoratorMetaData(DecoratorMetaData):
    template: str

    def __init__(self, template: str):
        self.type = "service"
        self.template = template
