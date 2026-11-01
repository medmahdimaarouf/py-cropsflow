from cropsflow.common.decorators import module

from .driver_manager import DriverManager

from .actions import *


@module(
    declarations=[
        SeleniumClickAction,
        SeleniumDriverBackAction,
        SeleniumDriverForwardAction,
        SeleniumDriverGetAction,
        SeleniumGetPageSourceDataAction,
        SeleniumGetPageTitleDataAction,
        SeleniumGetPageUrlDataAction,
        SeleniumDriverGetAction
    ],
    exports=[
        SeleniumClickAction,
        SeleniumDriverBackAction,
        SeleniumDriverForwardAction,
        SeleniumDriverGetAction,
        SeleniumGetPageSourceDataAction,
        SeleniumGetPageTitleDataAction,
        SeleniumGetPageUrlDataAction,
        SeleniumDriverGetAction
    ],
    providers=[
        DriverManager
    ]
)
class SeleniumModule:
    def __init__(self):
        pass
