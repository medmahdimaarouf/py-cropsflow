from common.schemas.docorator_metadata import DecoratorMetaData


class DataPipeDecoratorMetaData(DecoratorMetaData):
    selector: str
    type = "datapipe"

    def __int__(self, selector: str):
        self.selector = selector
