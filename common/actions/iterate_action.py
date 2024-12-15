from typing import Iterable, Any

from common.abstracts import Action
from common.abstracts.logger import Logger
from common.abstracts.task_context import TaskContext
from common.decorators import action, option


@action(selector="iterate")
class IterateAction(Action):
    it: Iterable[Any] = []

    def __init__(self):
        super().__init__()
        self.of = []

    @option(name='of', required=True)
    def set_name(self, of: Iterable[Any] = []):
        self.of = of

    async def run(self, context: TaskContext, logger: Logger = None) -> TaskContext:
        for i in self.of:
            await self.next(context)
        return context
