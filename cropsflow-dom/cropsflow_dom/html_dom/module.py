from cropsflow.common.decorators import module

from cropsflow_dom.html_dom.actions import HTMLHasChildAction, HTMLSelectAllAction, HTMLSelectFirstAction, \
    HTMLGetAttributeDataAction, HTMLGetTextContentPipe
from cropsflow_dom.html_dom.services import HtmlService


@module(
    providers=[HtmlService],
    declarations=[
        HTMLHasChildAction,
        HTMLSelectAllAction,
        HTMLSelectFirstAction,
        HTMLGetAttributeDataAction,
        HTMLGetTextContentPipe
    ],
    exports=[
        HTMLHasChildAction,
        HTMLSelectAllAction,
        HTMLSelectFirstAction,
        HTMLGetAttributeDataAction,
        HTMLGetTextContentPipe
    ]
)
class HTMLModule:
    pass
