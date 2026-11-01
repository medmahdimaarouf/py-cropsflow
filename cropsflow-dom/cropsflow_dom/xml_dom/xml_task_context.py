from dataclasses import dataclass
from typing import List, Optional

from ..dom_task_context import DOMTaskContext
from xml.etree import ElementTree


@dataclass
class XMLTaskContext(DOMTaskContext[ElementTree.Element]):
    @staticmethod
    def fromstring(source: str) -> "XMLTaskContext":
        """Creates an XMLTaskContext from a string."""
        return XMLTaskContext(element=ElementTree.fromstring(source))

    @staticmethod
    def parse(path: str) -> "XMLTaskContext":
        """Creates an XMLTaskContext by parsing an XML file from a path."""
        return XMLTaskContext(element=ET.parse(path).getroot())

    def find_elements_by_tag(self, tag: str) -> List[ElementTree.Element]:
        """Finds elements by their tag name."""
        return self.element.findall(tag)

    def find_elements_by_xpath(self, xpath: str) -> List[ElementTree.Element]:
        """Finds elements using an XPath query."""
        return self.element.xpath(xpath)

    def get_element_by_id(self, id: str) -> Optional[ElementTree.Element]:
        """Finds an element by its ID attribute."""
        return self.element.xpath(f"//*[@id='{id}']")[0] if self.element.xpath(f"//*[@id='{id}']") else None

    def get_text(self, xpath: str = None) -> str:
        """Gets all text content from the XML document."""
        return ''.join(self.element.itertext())

    def get_attribute(self, attribute: str, xpath: str = None) -> Optional[str]:
        """Retrieves the value of a specific attribute from an element found by XPath."""
        elements = self.element if xpath is None else self.find_elements_by_xpath(xpath)
        return elements[0].get(attribute) if elements and attribute in elements[0].attrib else None

    def set_attribute(self, attribute: str, value: str, xpath: str = None) -> None:
        """Sets an attribute on elements found by XPath."""
        for element in self.element if xpath is None else self.find_elements_by_xpath(xpath):
            element.set(attribute, value)

    def remove_element(self, xpath: str) -> None:
        """Removes elements found by XPath."""
        for element in self.find_elements_by_xpath(xpath):
            parent = element.getparent()
            if parent is not None:
                parent.remove(element)

    def append_element(self, parent_xpath: str, new_element: ElementTree.Element) -> None:
        """Appends a new element as a child to a parent element found by XPath."""
        parents = self.find_elements_by_xpath(parent_xpath)
        if parents:
            parents[0].append(new_element)

    def to_string(self, pretty: bool = False) -> str:
        """Converts the XML document back to a string."""
        return ET.tostring(self.element, pretty_print=pretty, encoding='unicode')
