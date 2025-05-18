from cropsflow.core import CropsFlow, TaskWorker
from app_module import AppModule
from tasks.app_task import AppTask
import asyncio


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
