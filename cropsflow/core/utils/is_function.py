from types import FunctionType, BuiltinFunctionType, MethodType


def is_function(obj) -> bool:
    return isinstance(obj, (FunctionType, BuiltinFunctionType, MethodType))
