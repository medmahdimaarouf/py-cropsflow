import pytest
from cropsflow.common import InjectionScope
from cropsflow.core import Injector
from cropsflow.core.testing import CropsFlowTesting

from cropsflow_dom.html_dom import HTMLTaskContext, HTMLModule
from cropsflow_dom.html_dom.actions.has_child_action import HTMLHasChildAction
from cropsflow_dom.html_dom.services import HtmlService


@pytest.fixture
async def injector():
    return await CropsFlowTesting.create_test_module(imports=[HTMLModule])


@pytest.fixture
def action(injector: Injector):
    return injector.resolve(token=HTMLHasChildAction, scope=InjectionScope.TRANSIENT)


@pytest.fixture
def html_content():
    return """
    <!DOCTYPE html>
    <html>
        <body>
            <div id="div1" class="item">Item 1</div>
            <div class="item">Item 2</div>
            <div class="item">Item 3</div>
        </body>
    </html>
    """


@pytest.fixture
def context(html_content):
    return HTMLTaskContext(element=HtmlService.parse(html_content))


@pytest.mark.asyncio
async def test_has_child_with_css_match(action: HTMLHasChildAction, context):
    context = await action.run(context, options={"css": ".item"})

    assert isinstance(context, HTMLTaskContext)
    assert context.element is not None


@pytest.mark.asyncio
async def test_has_child_with_xpath_match(action: HTMLHasChildAction, context):
    result = await action.run(context, options={"xpath": '//*[@id="div1"]'})

    assert isinstance(result, HTMLTaskContext)
    assert result.element.get("id") == "div1"


@pytest.mark.asyncio
async def test_has_child_with_no_match(action: HTMLHasChildAction, context):
    result = await action.run(context, options={"css": ".not-found"})

    assert result is context  # fallback to original context


@pytest.mark.asyncio
async def test_has_child_with_no_selectors(action: HTMLHasChildAction, context):
    with pytest.raises(Exception):
        await action.run(context, options={})
