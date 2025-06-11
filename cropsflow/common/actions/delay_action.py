from __future__ import annotations

from asyncio import sleep
from typing import Dict, Any

from ..abstracts import Action, TaskContext
from ..decorators import action, option


@action(selector="sleep")
@option(key='seconds', meta_type=int)
class DelayAction(Action):

    async def run(self, context: TaskContext, options: Dict[str, Any] = {}) -> TaskContext:
        seconds = int(options.get('seconds', 5))
        await sleep(seconds)
        await self.next(context)
