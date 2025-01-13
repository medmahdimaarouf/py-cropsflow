import asyncio

from cropsflow.common import CommonModule, Init
from cropsflow.common.decorators import module, inject, FactoryProviderMetaData, ValueProviderMetaData
from cropsflow.core import CropsFlow, TaskWorker
from tasks import *


@inject(arg_name='v', token='p1')
def provider_function(v: int) -> str:
    return 'i am provider_function ' + str(v)


@module(
    declarations=[AppTask],
    imports=[CommonModule],
    providers=[
        ValueProviderMetaData(provide="p1", use_value=1),
        FactoryProviderMetaData(provide='provider_function', use_factory=provider_function)
    ]
)
class AppModule(Init):
    @inject(arg_name="i1", token="p1")
    def init(self, i1: int) -> None:
        print("init : ", i1)

    def __init__(self):
        pass


async def start():
    app = await CropsFlow.start(AppModule)
    print("Starting")
    worker: TaskWorker = app.engine.create_worker(AppTask)
    # await worker.start_async()
    worker.start()
    worker.stop()
    print("Finished")


if __name__ == '__main__':
    asyncio.run(start())
