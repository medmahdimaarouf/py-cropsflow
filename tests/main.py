from app_module import AppModule
from cropsflow.platforms import CropsFlow, CropsFlowGateway
from tasks.app_task import AppTask
import asyncio


async def start():
    return await CropsFlowGateway.start(AppModule)


if __name__ == '__main__':
    app = asyncio.run(start())
