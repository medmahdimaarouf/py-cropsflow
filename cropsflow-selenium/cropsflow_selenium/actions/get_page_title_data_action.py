from typing import Dict, Any

from cropsflow import TaskContext
from cropsflow.common import DataAction, action

from ..context import SeleniumTaskContext


@action(selector='selenium-get-page-title')
class SeleniumGetPageTitleDataAction(DataAction[str, SeleniumTaskContext]):
    async def run(self, context: SeleniumTaskContext, options: Dict[str, Any]) -> TaskContext:
        self._data = context.driver.title
        return context
