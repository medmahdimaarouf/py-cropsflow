from .decorators.module import module
from .actions import *
from .pipes import *


@module(
    declarations=[
        DelayAction,
        IterateAction
    ],
    exports=[
        DelayAction,
        IterateAction
    ]
)
class CommonModule:
    pass
