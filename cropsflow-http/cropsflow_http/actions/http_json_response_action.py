import json
from typing import Dict, Any

from cropsflow import action, Action
from cropsflow_dom.html_dom import HTMLTaskContext

from ..http_response_context import HttpResponseTaskContext, HttpJSONResponseTaskContext
from ..services import HttpRequestsService


@action(selector='http-json-response')
class HttpJSONResponseAction(Action):
    http_requests_service: HttpRequestsService = None

    def __init__(self, http_requests_service: HttpRequestsService):
        self.http_requests_service = http_requests_service

    async def run(self, context: HttpResponseTaskContext, options: Dict[str, Any] = {}) -> HTMLTaskContext:
        return HttpJSONResponseTaskContext(json.loads(context.text))
