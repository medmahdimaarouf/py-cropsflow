from cropsflow.common import CommonModule, Init
from cropsflow.common.decorators import module, inject, FactoryProviderMetaData, ValueProviderMetaData


@inject(arg_name='v', token='p1')
def provider_function(v: int) -> str:
    return 'i am provider_function ' + str(v)


@module(
    # declarations=[AppTask],
    imports=[CommonModule],
    providers=[
        ValueProviderMetaData(provide="p1", use_value=1),
        FactoryProviderMetaData(provide='provider_function', use_factory=provider_function)
    ],
    exports=['p1']
)
class AppModule(Init):
    @inject(arg_name="i1", token="p1")
    async def init(self, i1: int) -> None:
        pass

    def __init__(self):
        pass
