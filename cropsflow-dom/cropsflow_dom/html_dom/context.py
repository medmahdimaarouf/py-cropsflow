from dataclasses import dataclass

from lxml import html

from cropsflow_dom.dom_task_context import DOMTaskContext


@dataclass
class HTMLTaskContext(DOMTaskContext[html.HtmlElement]):
    def __init__(self, element: html.HtmlElement):
        super().__init__(element=element)
