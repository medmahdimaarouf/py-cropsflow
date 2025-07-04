import asyncio

from app_module import AppModule
from cropsflow.platforms import CropsFlowRemote
from cropsflow.orchestrator import Worker
from cropsflow.platforms import CropsFlow
from tests.tasks.app_task import AppTask


async def start():
    application = await CropsFlowRemote.start(module=AppModule, port=8000, allow_origins=['http://localhost:4200'])
    # worker: Worker = application.get_orchestrator().create_worker(meta_type=AppTask)
    # worker.start()
    return application


if __name__ == '__main__':
    try:
        app = asyncio.run(start())
    except asyncio.CancelledError:
        pass
    except KeyboardInterrupt:
        pass
