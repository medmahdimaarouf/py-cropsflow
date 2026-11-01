from cropsflow_json.actions import *
from cropsflow.common.decorators import module


@module(
    declarations=[JSONParse],
    exports=[JSONParse]
)
class JSONModule:
    pass
