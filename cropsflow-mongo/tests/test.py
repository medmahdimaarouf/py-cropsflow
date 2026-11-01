import asyncio

from cropsflow import CropsFlow
from cropsflow.orchestrator import Orchestrator, Worker

from tests.test_module import TestModule
from tests.test_task import TestTask


async def start():
    app = await CropsFlow.start(TestModule)
    orchestrator: Orchestrator = app.get_orchestrator()
    worker: Worker = orchestrator.create_worker(TestTask)
    worker.start()


if __name__ == '__main__':
    asyncio.run(start())
