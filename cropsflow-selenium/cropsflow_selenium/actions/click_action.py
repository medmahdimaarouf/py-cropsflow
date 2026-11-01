from typing import Dict, Any

from cropsflow import TaskContext
from cropsflow.common import action, option, Action
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from ..context import SeleniumTaskContext


@action(selector='selenium-click')
@option(key='xpath', meta_type=str, default=None)
@option(key='css', meta_type=str, default=None)
@option(key='id', meta_type=str, default=None)
@option(key='tag', meta_type=str, default=None)
class SeleniumClickAction(Action[SeleniumTaskContext]):

    async def run(self, context: SeleniumTaskContext, options: Dict[str, Any]) -> TaskContext:
        selectors = {
            'xpath': options.get('xpath'),
            'css': options.get('css'),
            'id': options.get('id'),
            'tag': options.get('tag')
        }

        provided = {k: v for k, v in selectors.items() if v is not None}

        if len(provided) == 0:
            raise ValueError("At least one selector must be provided (xpath, css, id, or tag).")

        if len(provided) > 1:
            raise ValueError(
                f"Only one selector must be provided, but multiple were given: {', '.join(provided.keys())}")

        web_element: WebElement = None

        if options.get('id', None) is not None:
            web_element = context.driver.find_element(By.ID, options.get('id'))

        if options.get('tag', None) is not None:
            web_element = context.driver.find_element(By.TAG_NAME, options.get('tag'))

        if options.get('css', None) is not None:
            web_element = context.driver.find_element(By.CSS_SELECTOR, options.get('css'))

        if options.get('xpath', None) is not None:
            web_element = context.driver.find_element(By.XPATH, options.get('xpath'))

        if web_element is not None:
            web_element.click()
            return context
        else:
            selector = provided.popitem()
            raise Exception(
                f"Could not find element by selector '{selector[0]}' value '{selector[1]}'")
