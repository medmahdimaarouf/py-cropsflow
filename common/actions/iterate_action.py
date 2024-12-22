from typing import Iterable, Any, List, Dict

from common.abstracts import Action
from common.abstracts.logger import Logger
from common.abstracts.task_context import TaskContext
from common.decorators import action, option


@action(selector="iterate")
@option(key='of', meta_type=List)
class IterateAction(Action):
    it: Iterable[Any] = []

    def __init__(self):
        super().__init__()

    async def run(self, context: TaskContext, options: Dict[str, Any] = None) -> TaskContext:
        for i in self.of:
            await self.next(context)
        return context
