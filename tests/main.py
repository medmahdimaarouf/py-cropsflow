from app_module import AppModule
from cropsflow.orchestrator import Worker
from cropsflow.platforms import CropsFlow, CropsFlowRemote
from tests.tasks.app_task import AppTask
import asyncio


async def start():
    application = await CropsFlow.start(AppModule)
    worker: Worker = application.get_orchestrator().create_worker(meta_type=AppTask)
    worker.start()
    return application


if __name__ == '__main__':
    app = asyncio.run(start())
