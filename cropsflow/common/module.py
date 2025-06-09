from .actions import *
from .pipes import *
from .decorators.module import module


@module(
    declarations=[
        DelayAction,
        IterateAction,
        CMDAction,
        MapPipe,
        ListPipe,
        IntegerPipe,
        TextPipe,
        DecimalPipe
    ],
    exports=[
        DelayAction,
        IterateAction,
        CMDAction,
        MapPipe,
        ListPipe,
        IntegerPipe,
        TextPipe,
        DecimalPipe
    ]
)
class CommonModule:
    pass
