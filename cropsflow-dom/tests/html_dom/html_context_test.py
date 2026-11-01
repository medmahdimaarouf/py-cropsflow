import pytest

from cropsflow_dom.html_dom import HTMLTaskContext
from cropsflow_dom.html_dom.services import HtmlService

html_source = """
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


@pytest.mark.parametrize('source', [html_source])
def test_instantiating_html_context(source: str):
    try:
        html_service: HtmlService = HtmlService()
        html_task_context: HTMLTaskContext = HTMLTaskContext(element=html_service.parse(source))
        assert html_task_context.element is not None
    except Exception as e:
        pytest.fail(f"HTMLTaskContext from string dom exception: {e}")
