from .actions import *
from .pipes import *
from .decorators.module import module


@module(
    declarations=[
        DelayAction,
        IterateAction,
        MapPipe,
        ListPipe
    ],
    exports=[
        DelayAction,
        IterateAction,
        MapPipe,
        ListPipe
    ]
)
class CommonModule:
    pass
