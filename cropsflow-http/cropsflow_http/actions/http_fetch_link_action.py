from typing import Dict, Any
from urllib.parse import urljoin

import requests
from cropsflow.common import action, Action, option, TaskContext
from cropsflow_dom.html_dom import HTMLTaskContext
from lxml import html

from ..http_response_context import HttpResponseTaskContext
from ..services import HttpRequestsService


@action(selector="http-fetch-link-action")
@option(key='base-url', meta_type=str, default='')
@option(key='xpath', meta_type=str, default=None)
@option(key='css', meta_type=str, default=None)
@option(key='href', meta_type=str, default='href')
@option(key='headers', meta_type=dict, default={})
@option(key='params', meta_type=dict, default={})
@option(key='cookies', meta_type=dict, default={})
@option(key='timeout', meta_type=int, default=5)
@option(key='allow_redirects', meta_type=bool, default=True)
class HttpFetchLinkAction(Action):
    http_requests_service: HttpRequestsService = None

    def __init__(self, http_requests_service: HttpRequestsService):
        self.http_requests_service = http_requests_service

    async def run(self, context: HTMLTaskContext, options: Dict[str, Any] = {}) -> TaskContext:
        base_url = options.get('base-url', '')
        xpath_selector: str = options.get('xpath', None)
        css_selector: str = options.get('css', None)
        href: str = options.get('href', 'href')
        headers = options.get("headers", None)
        params = options.get("params", None)
        cookies = options.get("cookies", None)
        timeout = options.get("timeout", None)
        allow_redirects = options.get("allow_redirects", False)
        html_element: html.HtmlElement = context.element
        if css_selector is not None:
            html_elements = context.find_elements_by_css(css_selector=css_selector)
            html_element = html_elements[0] if len(html_elements) > 0 else None
        elif xpath_selector is not None:
            html_elements = list(context.find_elements_by_xpath(xpath_selector=xpath_selector))
            html_element = html_elements[0] if len(html_elements) > 0 else None
        if html_element is None:
            raise Exception(
                f"Could not find element by selector {'css' if css_selector else 'xpath'}: \
                    '{css_selector or xpath_selector}'")
        element_href: str = html_element.get(href) if html_element is not None else None
        if element_href is not None and len(element_href) > 0:
            url: str = urljoin(base_url, element_href)
            response = requests.get(url=url, params=params,
                                    headers=headers or HttpRequestsService.get_mimic_browser_headers(url=url),
                                    cookies=cookies,
                                    timeout=timeout,
                                    allow_redirects=allow_redirects
                                    )
            response.raise_for_status()
            response.close()
            return HttpResponseTaskContext(headers=response.headers, content=response.content,
                                           cookies=response.cookies, ok=response.ok,
                                           status_code=response.status_code, text=response.text)
        else:
            raise Exception(f"Could not find url attribute by '{href}'")
