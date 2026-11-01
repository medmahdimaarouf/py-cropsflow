import pytest
from lxml import html

from cropsflow_dom.html_dom.services import HtmlService

sample_html = """
<!DOCTYPE html>
<html>
  <body>
    <div id="main" class="container">
      <p class="text">Hello</p>
      <p class="text">World</p>
      <span data-custom="value">Span</span>
    </div>
  </body>
</html>
"""


@pytest.fixture
def root_element():
    return HtmlService.parse(sample_html)


def test_parse_valid_html():
    element = HtmlService.parse(sample_html)
    assert element is not None
    assert isinstance(element, html.HtmlElement)


def test_parse_invalid_html():
    with pytest.raises(Exception):
        HtmlService.parse(None)  # invalid input should raise


def test_get_element_by_id_found(root_element):
    div = HtmlService.get_element_by_id(root_element, "main")
    assert div is not None
    assert div.tag == "div"


def test_get_element_by_id_not_found(root_element):
    element = HtmlService.get_element_by_id(root_element, "nope")
    assert element is None


def test_find_elements_by_tag(root_element):
    ps = HtmlService.find_elements_by_tag(root_element, "p")
    assert len(ps) == 2
    assert all(p.tag == "p" for p in ps)


def test_find_elements_by_tag_none():
    assert HtmlService.find_elements_by_tag(None, "p") is None


def test_find_elements_by_class_found(root_element):
    result = HtmlService.find_elements_by_class(root_element, "text")
    assert len(result) == 2


def test_find_elements_by_class_not_found(root_element):
    result = HtmlService.find_elements_by_class(root_element, "none")
    assert result == []


def test_find_elements_by_xpath_found(root_element):
    elements = HtmlService.find_elements_by_xpath(root_element, "//p")
    assert len(elements) == 2


def test_find_elements_by_xpath_invalid(root_element):
    with pytest.raises(Exception):
        HtmlService.find_elements_by_xpath(root_element, "not xpath")


def test_find_elements_by_css_found(root_element):
    result = HtmlService.find_elements_by_css(root_element, ".text")
    assert len(result) == 2


def test_get_text(root_element):
    div = HtmlService.get_element_by_id(root_element, "main")
    text = HtmlService.get_text(div)
    assert "Hello" in text and "World" in text


def test_get_text_none():
    assert HtmlService.get_text(None) is None


def test_set_and_get_attribute(root_element):
    span = HtmlService.find_elements_by_tag(root_element, "span")[0]
    HtmlService.set_attribute(span, "id", "span1")
    assert HtmlService.get_attribute(span, "id") == "span1"


def test_get_attribute_not_found(root_element):
    div = HtmlService.get_element_by_id(root_element, "main")
    assert HtmlService.get_attribute(div, "nonexistent") is None


def test_to_string(root_element):
    div = HtmlService.get_element_by_id(root_element, "main")
    html_str = HtmlService.to_string(div)
    assert "<div" in html_str and "</div>" in html_str


def test_all_methods_with_none():
    # All methods should return None or empty list when given None safely
    assert HtmlService.get_element_by_id(None, "id") is None
    assert HtmlService.find_elements_by_tag(None, "div") is None
    assert HtmlService.find_elements_by_class(None, "class") is None
    assert HtmlService.find_elements_by_xpath(None, "//div") is None
    assert HtmlService.find_elements_by_css(None, ".class") is None
    assert HtmlService.get_text(None) is None
    assert HtmlService.get_attribute(None, "id") is None
    assert HtmlService.set_attribute(None, "id", "val") is None
    assert HtmlService.to_string(None) is None
