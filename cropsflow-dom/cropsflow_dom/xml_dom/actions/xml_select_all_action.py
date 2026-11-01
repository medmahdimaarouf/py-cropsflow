from typing import Dict, Any

from cropsflow.common import Action, action, option, TaskContext
from ..xml_task_context import XMLTaskContext


@action(selector='xml-select_all')
@option(key='xpath', meta_type=str, default=None)
class XMLSelectAllAction(Action):
    async def run(self, context: XMLTaskContext, options: Dict[str, Any] = {}) -> TaskContext:
        xpath: str = options.get('xpath', None)
        for element in context.find_elements_by_xpath(xpath):
            await self.next(XMLTaskContext(element=element))
        await self.next()
