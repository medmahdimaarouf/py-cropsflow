from __future__ import annotations

from asyncio import sleep
from ctypes import Union
from typing import Dict, Any

from common.abstracts import Action, Logger
from common.abstracts.task_context import TaskContext
from common.decorators import action, option


@action(selector="sleep")
@option(key='seconds', meta_type=int)
class DelayAction(Action):
    def __init__(self):
        super().__init__()

    async def run(self, context: TaskContext, options: Dict[str, Any] = {}) -> TaskContext:
        seconds = int(options.get('seconds', 5))
        await sleep(seconds)
        await self.next(context)
