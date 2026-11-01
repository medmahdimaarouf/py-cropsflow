from typing import Dict, Any

from cropsflow import TaskContext
from cropsflow.common import DataAction, action

from ..context import SeleniumTaskContext


@action(selector='selenium-get-page-source')
class SeleniumGetPageSourceDataAction(DataAction[str, SeleniumTaskContext]):
    async def run(self, context: SeleniumTaskContext, options: Dict[str, Any]) -> TaskContext:
        self._data = context.driver.page_source
        return context
