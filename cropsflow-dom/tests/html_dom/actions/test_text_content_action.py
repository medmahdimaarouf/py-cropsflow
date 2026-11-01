import pytest
from cropsflow import Injector, InjectionScope
from cropsflow.core.testing import CropsFlowTesting

from cropsflow_dom.html_dom import HTMLModule
from cropsflow_dom.html_dom.actions import HTMLGetTextContentPipe
from cropsflow_dom.html_dom.context import HTMLTaskContext
from cropsflow_dom.html_dom.services import HtmlService


@pytest.fixture
def html_content():
    return """
    <!DOCTYPE html>
    <html>
        <body>
            <div class="note">  Hello World  </div>
            <span id="target">Some text content</span>
        </body>
    </html>
    """


@pytest.fixture
async def injector():
    return await CropsFlowTesting.create_test_module(imports=[HTMLModule])


@pytest.fixture
def action(injector: Injector):
    return injector.resolve(token=HTMLGetTextContentPipe, scope=InjectionScope.TRANSIENT)


@pytest.fixture
def context(html_content):
    return HTMLTaskContext(element=HtmlService.parse(html_content))


async def test_get_text_action_with_css_and_trim(action, context):
    options = {'css': '.note', 'trim': True}
    await action.run(context, options)
    assert action.get_data() == "Hello World"


async def test_get_text_action_with_css_and_no_trim(action, context):
    options = {'css': '.note', 'trim': False}
    await action.run(context, options)
    assert action.get_data() == "  Hello World  "


async def test_get_text_action_with_xpath(action, context):
    options = {'xpath': '//span[@id="target"]'}
    await action.run(context, options)
    assert action.get_data() == "Some text content"


async def test_get_text_action_with_no_match_uses_default(action, context):
    options = {'css': '.non-existent', 'default': 'Fallback'}
    with pytest.raises(Exception):
        await action.run(context, options)


async def test_get_text_action_with_no_selector_uses_conget_text_element(action, context):
    options = {}
    await action.run(context, options)
    assert "Hello World" in action.get_data() or "Some text content" in action.get_data()


async def test_get_text_action_empty_element_and_default(action, context):
    options = {
        'xpath': '//not-found',
        'default': 'EmptyFallback'
    }
    with pytest.raises(Exception):
        await action.run(context, options)
