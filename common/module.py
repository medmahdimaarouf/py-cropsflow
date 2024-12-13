from .decorators.module import PrxModule
from .actions import *
from .pipes import *


@PrxModule(
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
