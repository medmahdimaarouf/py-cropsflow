import pytest
from cropsflow import Injector, InjectionScope
from cropsflow.core.testing import CropsFlowTesting

from cropsflow_dom.html_dom import HTMLModule
from cropsflow_dom.html_dom.actions import HTMLGetAttributeDataAction
from cropsflow_dom.html_dom.context import HTMLTaskContext
from cropsflow_dom.html_dom.services import HtmlService


@pytest.fixture
def html_content():
    return """
    <!DOCTYPE html>
    <html>
        <body>
            <div class="target" data-info="  value with spaces  "></div>
            <span id="unique" title="Hello World"></span>
        </body>
    </html>
    """


@pytest.fixture
async def injector():
    return await CropsFlowTesting.create_test_module(imports=[HTMLModule])


@pytest.fixture
def action(injector: Injector):
    return injector.resolve(token=HTMLGetAttributeDataAction, scope=InjectionScope.TRANSIENT)


@pytest.fixture
def context(html_content):
    return HTMLTaskContext(element=HtmlService.parse(html_content))


async def test_attribute_pipe_with_css_selector_and_trim(action, context):
    options = {'name': 'data-info', 'css': '.target', 'trim': True}
    await action.run(context=context, options=options)
    assert action.get_data() == "value with spaces"


async def test_attribute_pipe_with_css_selector_without_trim(action, context):
    options = {'name': 'data-info', 'css': '.target', 'trim': False}
    await action.run(context, options)
    assert action.get_data() == "  value with spaces  "


async def test_attribute_pipe_with_xpath_selector(action, context):
    options = {'name': 'title', 'xpath': '//span[@id="unique"]'}
    await action.run(context, options)
    assert action.get_data() == "Hello World"


async def test_attribute_pipe_with_no_match_but_default(action, context):
    options = {'name': 'nonexistent', 'css': '.target', 'default': 'Default Value'}
    with pytest.raises(Exception):
        await action.run(context, options)


async def test_attribute_pipe_with_no_selector_uses_context_element(action, context):
    options = {'name': 'data-info'}
    with pytest.raises(Exception):
        await action.run(context, options)
    # context.element is root <html>, it has no 'data-info'


async def test_attribute_pipe_with_missing_attribute_and_no_default(action, context):
    options = {'name': 'missing', 'css': '.target'}
    with pytest.raises(Exception):
        await action.run(context, options)
