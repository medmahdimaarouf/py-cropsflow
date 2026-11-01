from typing import Dict, Any

from cropsflow import TaskContext
from cropsflow.common import action, option, Action
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from ..context import SeleniumTaskContext
from ..driver_manager import DriverManager


@action(selector='selenium-driver-get')
@option(key='url', meta_type=str, required=True)
class SeleniumDriverGetAction(Action[SeleniumTaskContext]):
    def __init__(self, driver_manager: DriverManager):
        self.driver_manager: DriverManager = driver_manager

    async def run(self, context: SeleniumTaskContext, options: Dict[str, Any]) -> TaskContext:
        url: str = options.get('url')
        self.driver_manager.driver.get(url=url)
