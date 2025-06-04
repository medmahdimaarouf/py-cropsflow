from typing import Dict, Any

from cropsflow import C, TaskContext
from cropsflow.common.decorators import action, option
from cropsflow.common import Action


@action(selector='raise-error')
@option(key='msg', default='Error with no message option value')
class RaiseErrorAction(Action):
    async def run(self, context: C, options: Dict[str, Any] = {}) -> TaskContext:
        raise Exception(options.get('msg'))
