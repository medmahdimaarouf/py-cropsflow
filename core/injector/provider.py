from .container import Container
from common.decorators import ProviderMetaData


class Provider(Container):
    def __init__(self, metadata: ProviderMetaData, host: Container = None):
        super().__init__(metadata=metadata, host=host)
