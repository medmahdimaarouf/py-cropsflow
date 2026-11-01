from typing import Dict, Any
from cropsflow import TaskContext
from cropsflow.common import action, option, Action
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json

from ..context import SeleniumTaskContext
from ..driver_manager import DriverManager


@action(selector='selenium-open-browser', auto_next=True)
@option(key='browser', meta_type=str, default='chrome')  # chrome, firefox, edge, safari, remote
@option(key='headless', meta_type=bool, default=False)
@option(key='window_size', meta_type=str, required=False)  # e.g. 1280,800
@option(key='user_agent', meta_type=str, required=False)
@option(key='proxy', meta_type=str, required=False)  # host:port
@option(key='binary_path', meta_type=str, required=False)
@option(key='args', meta_type=str, required=False)  # comma-separated flags
@option(key='capabilities', meta_type=str, required=False)  # JSON string
@option(key='remote_url', meta_type=str, required=False)
@option(key='emulate_device', meta_type=str, required=False)  # e.g. "iPhone X"
class SeleniumOpenBrowserAction(Action[SeleniumTaskContext]):
    def __init__(self, driver_manager: DriverManager):
        self.driver_manager: DriverManager = driver_manager

    async def run(self, context: SeleniumTaskContext, options: Dict[str, Any]) -> TaskContext:
        browser = options.get('browser', 'chrome').lower()
        headless = options.get('headless', False)
        window_size = options.get('window_size')
        user_agent = options.get('user_agent')
        proxy = options.get('proxy')
        binary_path = options.get('binary_path')
        emulate_device = options.get('emulate_device')
        remote_url = options.get('remote_url')
        custom_args = [a.strip() for a in options.get('args', '').split(',') if a.strip()]
        caps = {}

        # Parse capabilities from JSON string (if provided)
        if options.get('capabilities'):
            try:
                caps = json.loads(options.get('capabilities'))
            except Exception as e:
                raise ValueError(f"Invalid capabilities JSON: {e}")

        driver: WebDriver = None

        if browser == 'chrome':
            opts = ChromeOptions()
            if headless:
                opts.add_argument('--headless')
            if window_size:
                opts.add_argument(f"--window-size={window_size}")
            if user_agent:
                opts.add_argument(f"--user-agent={user_agent}")
            if proxy:
                opts.add_argument(f'--proxy-server={proxy}')
            if binary_path:
                opts.binary_location = binary_path
            for arg in custom_args:
                opts.add_argument(arg)
            if emulate_device:
                opts.add_experimental_option("mobileEmulation", {"deviceName": emulate_device})
            driver = webdriver.Chrome(options=opts, desired_capabilities=caps or opts.to_capabilities())

        elif browser == 'firefox':
            opts = FirefoxOptions()
            if headless:
                opts.add_argument('--headless')
            if binary_path:
                opts.binary_location = binary_path
            for arg in custom_args:
                opts.add_argument(arg)
            profile = webdriver.FirefoxProfile()
            if user_agent:
                profile.set_preference("general.useragent.override", user_agent)
            if proxy:
                host, port = proxy.split(":")
                profile.set_preference("network.proxy.type", 1)
                profile.set_preference("network.proxy.http", host)
                profile.set_preference("network.proxy.http_port", int(port))
            driver = webdriver.Firefox(options=opts, firefox_profile=profile, desired_capabilities=caps)

        elif browser == 'edge':
            opts = EdgeOptions()
            if headless:
                opts.add_argument('--headless')
            if binary_path:
                opts.binary_location = binary_path
            for arg in custom_args:
                opts.add_argument(arg)
            driver = webdriver.Edge(options=opts, desired_capabilities=caps or opts.to_capabilities())

        elif browser == 'safari':
            if headless:
                raise ValueError("Safari does not support headless mode")
            driver = webdriver.Safari(desired_capabilities=caps)

        elif browser == 'remote':
            if not remote_url:
                raise ValueError("Missing required 'remote_url' for remote browser")
            default_caps = DesiredCapabilities.CHROME.copy()
            default_caps.update(caps)
            driver = webdriver.Remote(command_executor=remote_url, desired_capabilities=default_caps)

        else:
            raise ValueError(f"Unsupported browser type: {browser}")

        return await self.next(SeleniumTaskContext(driver=driver))
