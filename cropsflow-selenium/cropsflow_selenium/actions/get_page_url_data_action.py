from typing import Dict, Any

from cropsflow import TaskContext
from cropsflow.common import DataAction, action

from ..context import SeleniumTaskContext


@action(selector='selenium-get-page-url')
class SeleniumGetPageUrlDataAction(DataAction[str, SeleniumTaskContext]):
    async def run(self, context: SeleniumTaskContext, options: Dict[str, Any]) -> TaskContext:
        self._data = context.driver.current_url
        return context
