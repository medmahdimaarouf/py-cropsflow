from common.schemas import DecoratorMetaData


class ServiceDecoratorMetaData(DecoratorMetaData):
    provide_in: str

    def __init__(self, provide_in: str = "root"):
        self.type = "service"
        self.provide_in = provide_in
