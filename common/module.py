from .decorators.module import PrxModule
from .actions import *
from .pipes import *


@PrxModule(
    declarations=[
        DelayAction,
        IterateAction
    ],
    imports=[
    ],
    providers=[
    ]
)
class CommonModule:
    pass
