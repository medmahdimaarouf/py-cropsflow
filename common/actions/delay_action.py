from __future__ import annotations

from asyncio import sleep
from ctypes import Union
from common.abstracts import Action, Logger, Option
from common.abstracts.task_context import TaskContext
from common.decorators import PrxAction


@PrxAction("sleep")
class DelayAction(Action):
    ms: Union[float | int] = 1000

    def __init__(self):
        super().__init__()
        self.ms = 1000

    @Option(label='ms', required=True)
    def set_name(self, ms: Union[float | int]):
        self.ms = ms

    async def run(self, context: TaskContext, logger: Logger = None) -> TaskContext:
        await sleep(self.ms)
        yield await self.next(context)
