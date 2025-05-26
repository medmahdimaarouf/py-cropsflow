from typing import Dict, Any

from cropsflow import C, TaskContext
from cropsflow.common import action, Action


@action(selector='stop')
class StopAction(Action):
    async def run(self, context: C, options: Dict[str, Any] = {}) -> TaskContext:
        pass
