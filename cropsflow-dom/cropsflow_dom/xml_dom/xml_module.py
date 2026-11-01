from cropsflow.common.decorators import module

from .actions import XMLSelectAllAction


@module(
    declarations=[XMLSelectAllAction],
    exports=[XMLSelectAllAction]
)
class XMLModule:
    pass
