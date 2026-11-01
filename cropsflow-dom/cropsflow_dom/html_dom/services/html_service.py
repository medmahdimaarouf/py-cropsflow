from typing import Optional, List

from cropsflow.common import service, InjectionScope
from lxml import html


@service(scope=InjectionScope.TRANSIENT)
class HtmlService:

    @classmethod
    def parse(cls, html_source: str) -> Optional[html.HtmlElement]:
        return html.fromstring(html=html_source)

    @classmethod
    def get_element_by_id(cls, element: html.HtmlElement, element_id: str) -> Optional[html.HtmlElement]:
        """Finds an element by its ID attribute."""
        find = element.get_element_by_id(element_id, None) if element is not None else None
        return find[0] if isinstance(find, list) else find

    @classmethod
    def find_elements_by_tag(cls, element: html.HtmlElement, tag_name: str) -> List[html.HtmlElement]:
        """Finds all elements with a specific tag."""
        return element.findall(f".//{tag_name}") if element is not None else None

    @classmethod
    def find_elements_by_class(cls, element: html.HtmlElement, class_name: str) -> List[html.HtmlElement]:
        """Finds all elements with a specific class name."""
        return list(element.cssselect(f'.{class_name}')) if element is not None else None

    @classmethod
    def find_elements_by_xpath(cls, element: html.HtmlElement, xpath: str) -> List[html.HtmlElement]:
        """Finds elements using an XPath expression."""
        return list(element.xpath(xpath)) if element is not None else None

    @classmethod
    def find_elements_by_css(cls, element: html.HtmlElement, css_selector: str) -> List[html.HtmlElement]:
        """Finds elements using a CSS selector."""
        return list(element.cssselect(css_selector)) if element is not None else None

    @classmethod
    def get_text(cls, element: html.HtmlElement) -> str:
        """Extracts all text content from the HTML document."""
        return element.text_content() if element is not None else None

    @classmethod
    def set_attribute(cls, element: html.HtmlElement, attribute: str, value: str) -> None:
        """Sets an attribute for element."""
        return element.set(attribute, value) if element is not None else None

    @classmethod
    def get_attribute(cls, element: html.HtmlElement, attribute: str) -> Optional[str]:
        """Gets the value of an attribute from the first element matching an XPath expression."""
        return element.get(attribute) if element is not None else None

    @classmethod
    def to_string(cls, element: html.HtmlElement, pretty_print: bool = True) -> str:
        """Serializes the HTML content to a string."""
        return html.tostring(element, pretty_print=pretty_print, encoding="unicode") if element is not None else None
