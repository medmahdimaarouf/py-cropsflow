from common import CommonModule, ValueProviderMetaData
from core.application_factory import ApplicationFactory

from common.decorators import inject, FactoryProviderMetaData, module
from tasks import *
import asyncio


@inject(arg_name='v', token='p1')
def provider_function(v: int) -> str:
    return 'i am provider_function ' + str(v)


@module(
    declarations=[AppTask],
    imports=[CommonModule],
    providers=[
        ValueProviderMetaData(provide="p1", use_value=1),
        FactoryProviderMetaData(provide='provider_function', use_factory=provider_function)
    ],
    exports=[]
)
class AppModule:
    def __init__(self):
        pass


def start():
    f = ApplicationFactory()
    app = f.init(AppModule)
    print("Starting")
    asyncio.run(app.engine.run(AppTask))


if __name__ == '__main__':
    start()
