from cropsflow.common import TaskContext
from selenium.webdriver.remote.webdriver import WebDriver


class SeleniumTaskContext(TaskContext):
    def __init__(self, driver: WebDriver):
        self.driver = driver
