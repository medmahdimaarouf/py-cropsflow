import pytest
from cropsflow import Injector, InjectionScope
from cropsflow.core.testing import CropsFlowTesting

from cropsflow_dom.html_dom import HTMLModule
from cropsflow_dom.html_dom.actions import HTMLSelectFirstAction
from cropsflow_dom.html_dom.context import HTMLTaskContext
from cropsflow_dom.html_dom.services import HtmlService


@pytest.fixture
def html_content():
    return """
    <!DOCTYPE html>
    <html>
        <body>
            <div class="item">Item 1</div>
            <div class="item">Item 2</div>
            <div class="item">Item 3</div>
        </body>
    </html>
    """


@pytest.fixture
async def injector():
    return await CropsFlowTesting.create_test_module(imports=[HTMLModule])


@pytest.fixture
def action(injector: Injector):
    return injector.resolve(token=HTMLSelectFirstAction, scope=InjectionScope.TRANSIENT)


@pytest.fixture
def context(html_content):
    return HTMLTaskContext(element=HtmlService.parse(html_content))


@pytest.mark.asyncio
async def test_select_first_with_css_selector(action: HTMLSelectFirstAction, context):
    options = {'css': '.item'}
    result = await action.run(context=context, options=options)
    assert isinstance(result, HTMLTaskContext)
    assert result.element.text == 'Item 1'


@pytest.mark.asyncio
async def test_select_first_with_xpath_selector(action: HTMLSelectFirstAction, context):
    options = {'xpath': '//div'}
    result = await action.run(context, options)
    assert isinstance(result, HTMLTaskContext)
    assert result.element.text == 'Item 1'


@pytest.mark.asyncio
async def test_select_first_with_invalid_css(action: HTMLSelectFirstAction, context):
    options = {'css': '.not-exist'}
    with pytest.raises(Exception):
        result = await action.run(context, options)


@pytest.mark.asyncio
async def test_select_first_with_invalid_xpath(action: HTMLSelectFirstAction, context):
    options = {'xpath': '//nothing'}
    with pytest.raises(Exception):
        result = await action.run(context, options)


@pytest.mark.asyncio
async def test_select_first_with_no_selector(action: HTMLSelectFirstAction, context):
    options = {}  # No selectors
    with pytest.raises(Exception):
        result = await action.run(context, options)
