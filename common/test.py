from asyncio import sleep

from common.decorators import PrxAction
from common.abstracts import Action
from common.abstracts import TaskContext, Logger


@PrxAction("qq")
class MyAction(Action):

    async def run(self, context: TaskContext, logger: Logger = None) -> TaskContext:
        sleep(2000)
        return context


print("ok")
