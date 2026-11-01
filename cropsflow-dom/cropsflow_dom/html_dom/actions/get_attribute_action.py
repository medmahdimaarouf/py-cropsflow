import html
from typing import Dict, Any

from cropsflow import TaskContext
from cropsflow.common import DataAction, action, option
from cropsflow.common.abstracts.data_action import C

from cropsflow_dom.html_dom.context import HTMLTaskContext
from cropsflow_dom.html_dom.services import HtmlService


@action(selector='html-get-attribute')
@option(key='name', meta_type=str, required=True)
@option(key='trim', meta_type=bool, default=True)
@option(key='xpath', meta_type=str, default=None)
@option(key='css', meta_type=str, default=None)
@option(key='default', meta_type=str, default=None)
@option(key='required', meta_type=bool, default=True)
class HTMLGetAttributeDataAction(DataAction[HTMLTaskContext, str]):
    def __init__(self, html_service: HtmlService):
        super().__init__(data=None)
        self.html_service = html_service

    async def run(self, context: C, options: Dict[str, Any]) -> TaskContext:
        name: str = options.get('name')
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

        attr_value: str = html_element.get(name)
        if attr_value is None and required:
            raise Exception(f"Required attribute value of '{name}'")
        attr_value = attr_value or default
        if attr_value is not None and trim:
            attr_value = attr_value.strip()
        self._data = attr_value
        return context
