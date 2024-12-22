from .actions import *
from .decorators.module import module


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
