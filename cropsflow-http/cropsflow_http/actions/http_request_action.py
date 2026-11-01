from typing import Dict, Any

import requests
from cropsflow.common import action, Action, option, TaskContext

from ..http_response_context import HttpResponseTaskContext
from ..services import HttpRequestsService


@action(selector="http-request")
@option(key='url', meta_type=str)
@option(key='method', meta_type=str, select=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'], default=None)
@option(key='headers', meta_type=dict, default={})
@option(key='params', meta_type=dict, default={})
@option(key='cookies', meta_type=dict, default={})
@option(key='timeout', meta_type=int, default=5)
@option(key='allow_redirects', meta_type=bool, default=True)
@option(key='body', meta_type=object, default=None)
class HttpRequestAction(Action):
    http_requests_service: HttpRequestsService = None

    def __init__(self, http_requests_service: HttpRequestsService):
        self.http_requests_service = http_requests_service

    async def run(self, context: TaskContext, options: Dict[str, Any] = {}) -> TaskContext:
        url = options.get('url')
        method = options.get('method')
        headers = options.get("headers", {})
        params = options.get("params", {})
        cookies = options.get("cookies", {})
        timeout = options.get("timeout", 5)
        allow_redirects = options.get("allow_redirects", False)
        body = options.get('body')
        response = requests.request(method=method, url=url, params=params, headers=headers, cookies=cookies,
                                    timeout=timeout, allow_redirects=allow_redirects, data=body)
        response.raise_for_status()
        response.close()
        return HttpResponseTaskContext(headers=response.headers, content=response.content(), cookies=response.cookies,
                                       ok=response.ok(), status_code=response.status_code, text=response.text())
