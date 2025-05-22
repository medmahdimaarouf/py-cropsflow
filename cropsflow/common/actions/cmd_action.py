from asyncio import sleep
from typing import Dict, Any
import subprocess
from ..abstracts import Action, TaskContext
from ..decorators import action, option


@action(selector="cmd")
@option(key='command', meta_type=str, required=True)
class DelayAction(Action):
    def __init__(self):
        super().__init__()

    async def run(self, context: TaskContext, options: Dict[str, Any] = {}) -> TaskContext:
        try:
            command: str = options.get("command")
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                check=True
            )
            self.set_data(result.stdout.strip())
            return await self.next(context)
        except subprocess.CalledProcessError as e:
            return context
        except Exception as ex:
            return context
