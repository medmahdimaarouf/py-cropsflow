import html
from typing import Dict, Any

from cropsflow import TaskContext
from cropsflow.common import DataAction, action, option
from cropsflow.common.abstracts.data_action import C

from cropsflow_dom.html_dom.context import HTMLTaskContext
from cropsflow_dom.html_dom.services import HtmlService


@action(selector='html-get-text-content')
@option(key='trim', meta_type=bool, default=True)
@option(key='xpath', meta_type=str, default=None)
@option(key='css', meta_type=str, default=None)
@option(key='default', meta_type=str, default=None)
@option(key='required', meta_type=bool, default=True)
class HTMLGetTextContentPipe(DataAction[HTMLTaskContext, str]):

    def __init__(self, html_service: HtmlService):
        super().__init__(data=None)
        self.html_service = html_service

    async def run(self, context: C, options: Dict[str, Any]) -> TaskContext:
        trim: str = options.get('trim', True)
        xpath_selector: str = options.get('xpath', None)
        css_selector: str = options.get('css', None)
        default: str = options.get('default', None)
        required: bool = options.get('required', True)

        html_element: html.HtmlElement = None

        if css_selector is not None:
            html_elements = self.html_service.find_elements_by_css(element=context.element, css_selector=css_selector)
            if not len(html_elements):
                raise Exception(f"Could not find element by css selector '{css_selector}'")
            else:
                html_element = html_elements[0]

        elif xpath_selector is not None:
            html_elements = self.html_service.find_elements_by_xpath(element=context.element, xpath=xpath_selector)
            if not len(html_elements):
                raise Exception(f"Could not find element by xpath selector '{xpath_selector}'")
            else:
                html_element = html_elements[0]
        else:
            html_element = context.element

        text_content: str = html_element.text_content()
        if text_content is None and required:
            raise Exception(f"Required attribute value for text content")
        text_content = text_content or default
        if text_content is not None and trim:
            text_content = text_content.strip()
        self._data = text_content
        return context
