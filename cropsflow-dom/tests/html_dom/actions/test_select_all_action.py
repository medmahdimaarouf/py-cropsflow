from typing import Dict, Any
from unittest.mock import AsyncMock

import pytest
from cropsflow import Injector, InjectionScope
from cropsflow.core.testing import CropsFlowTesting

from cropsflow_dom.html_dom import HTMLModule
from cropsflow_dom.html_dom.actions import HTMLSelectAllAction
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
    return injector.resolve(token=HTMLSelectAllAction, scope=InjectionScope.TRANSIENT)


@pytest.fixture
def context(html_content):
    return HTMLTaskContext(element=HtmlService.parse(html_content))


@pytest.mark.asyncio
async def test_select_all_with_css_selector(action: HTMLSelectAllAction, context):
    action.next = AsyncMock()

    options: Dict[str, Any] = {'css': '.item'}
    result = await action.run(context, options)

    assert isinstance(result, HTMLTaskContext)
    assert action.next.call_count == 3

    # Verify each call used XMLTaskContext
    for call_args in action.next.call_args_list:
        assert isinstance(call_args.args[0], HTMLTaskContext)


@pytest.mark.asyncio
async def test_select_all_with_next_call(action: HTMLSelectAllAction, context):
    auto_next = AsyncMock()

    async def next_call_back(ctx: HTMLTaskContext):
        print(ctx.element.text_content())
        assert isinstance(ctx, HTMLTaskContext)
        assert ctx.element.tag == 'div'
        auto_next()

    action.next = next_call_back

    options: Dict[str, Any] = {'css': '.item'}
    next_context = await action.run(context, options)

    assert isinstance(next_context, HTMLTaskContext)
    assert auto_next.call_count == 3
    assert len(auto_next.call_args_list) == 3


@pytest.mark.asyncio
async def test_select_all_with_xpath_selector(action: HTMLSelectAllAction, context):
    action.next = AsyncMock()

    options: Dict[str, Any] = {'xpath': '//div[@class="item"]'}
    result = await action.run(context, options)

    assert isinstance(result, HTMLTaskContext)
    assert action.next.call_count == 3


@pytest.mark.asyncio
async def test_select_all_with_no_matches(action: HTMLSelectAllAction, context):
    action.next = AsyncMock()

    options: Dict[str, Any] = {'css': '.not-exist'}
    result = await action.run(context, options)

    assert isinstance(result, HTMLTaskContext)
    action.next.assert_not_called()


@pytest.mark.asyncio
async def test_select_all_with_no_selectors(action: HTMLSelectAllAction, context):
    action.next = AsyncMock()

    options = {}
    with pytest.raises(Exception):
        result = await action.run(context, options)
