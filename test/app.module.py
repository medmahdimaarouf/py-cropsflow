import asyncio
import cProfile

from common import CommonModule, ValueProviderMetaData
from common.decorators import inject, FactoryProviderMetaData, module
from core import CropsFlow
from core.engine import TaskWorker
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
class AppModule:
    def __init__(self):
        pass


async def start():
    app = CropsFlow.start(AppModule)
    print("Starting")
    worker: TaskWorker = app.engine.create_worker(AppTask)
    #asyncio.run(worker.start_async())
    worker.start()
    await asyncio.sleep(4)
    print("Finished")


if __name__ == '__main__':
    asyncio.run(start())
