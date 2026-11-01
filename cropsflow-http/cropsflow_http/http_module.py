from cropsflow.common.decorators import module
from cropsflow_dom import DOMModule
from cropsflow_json import JSONModule

from .actions import *
from .services import HttpRequestsService


@module(
    providers=[
        HttpRequestsService
    ],
    declarations=[
        HttpRequestAction,
        HttpGetAction,
        HttpPostAction,
        HttpDeleteAction,
        HttpPutAction,
        HttpHTMLResponseAction,
        HttpFetchLinkAction
    ],
    imports=[
        DOMModule,
        JSONModule
    ],
    exports=[
        HttpRequestAction,
        HttpGetAction,
        HttpPostAction,
        HttpDeleteAction,
        HttpPutAction,
        HttpHTMLResponseAction,
        HttpFetchLinkAction
    ]
)
class HttpModule:
    pass
