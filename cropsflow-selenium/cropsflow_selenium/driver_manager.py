from cropsflow.common import service, InjectionScope
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver


@service(scope=InjectionScope.DEFAULT)
class DriverManager:
    def __init__(self):
        self.driver: WebDriver = None

    def chrome(self, options: Options = Options()) -> WebDriver:
        self.driver = webdriver.Chrome(options=options)

    def get_driver(self):
        return self.driver

    def close(self):
        if self.driver:
            self.driver.quit()
