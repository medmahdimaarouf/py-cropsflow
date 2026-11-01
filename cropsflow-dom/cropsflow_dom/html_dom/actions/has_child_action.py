from typing import Dict, Any

from cropsflow.common import Action, action, option, TaskContext

from ..context import HTMLTaskContext
from ..services import HtmlService


@action(selector='html-has-child', auto_next=False)
@option(key='xpath', meta_type=str, default=None)
@option(key='css', meta_type=str, default=None)
class HTMLHasChildAction(Action):
    def __init__(self, html_service: HtmlService):
        self.html_service = html_service

    async def run(self, context: HTMLTaskContext, options: Dict[str, Any] = {}) -> TaskContext:
        xpath_selector: str = options.get('xpath', None)
        css_selector: str = options.get('css', None)

        html_elements = []

        if css_selector is not None:
            html_elements = self.html_service.find_elements_by_css(element=context.element, css_selector=css_selector)
        elif xpath_selector is not None:
            html_elements = self.html_service.find_elements_by_xpath(element=context.element, xpath=xpath_selector)
        else:
            raise Exception("Neither 'xpath' or 'css' selection pattern was provided")

        if len(html_elements) > 0:
            await self.next(context=HTMLTaskContext(element=html_elements[0]))
        return context
