from inspect import signature, Parameter
from typing import Type, Any, List, Dict, Callable
from cropsflow.common.constants import *
from cropsflow.common.decorators import ModuleDecoratorMetaData, ActionDecoratorMetaData, DataPipeDecoratorMetaData, \
    ServiceDecoratorMetaData, TaskDecoratorMetaData, InjectionScope, InjectMetaData, FactoryProviderMetaData, \
    DecoratorMetaDataType
from cropsflow.common.decorators.option import Option


def isDecorated(meta_type: Type[Any], watermark: str) -> bool:
    return watermark in getattr(meta_type, DECORATOR_WATERMARKS, [])


def getDecorators(meta_type: Type[Any]) -> List[str]:
    return getattr(meta_type, DECORATOR_WATERMARKS, [])


def scanModuleMetaData(meta_type: Type[Any]) -> ModuleDecoratorMetaData:
    if isDecorated(meta_type, MODULE_WATERMARK):
        return ModuleDecoratorMetaData(
            target=meta_type,
            declarations=getattr(meta_type, MODULE_DECORATOR_DECLARATIONS_KEY, []),
            imports=getattr(meta_type, MODULE_DECORATOR_IMPORTS_KEY, []),
            providers=getattr(meta_type, MODULE_DECORATOR_PROVIDERS_KEY, []),
            exports=getattr(meta_type, MODULE_DECORATOR_EXPORTS_KEY, [])
        )
    else:
        raise Exception(meta_type.__name__ + " is not a @Module")


def scanActionMetaData(meta_type: Type[Any]) -> ActionDecoratorMetaData:
    if isDecorated(meta_type, ACTION_WATERMARK):
        return ActionDecoratorMetaData(target=meta_type, selector=getattr(meta_type, ACTION_DECORATOR_SELECTOR_KEY, ""),
                                       auto_next=getattr(meta_type, ACTION_DECORATOR_AUTO_NEXT_KEY, False))
    else:
        raise Exception(meta_type.__name__ + " is not an @Action")


def scanDataPipeMetaData(meta_type: Type[Any]) -> DataPipeDecoratorMetaData:
    if isDecorated(meta_type, PIPE_WATERMARK):
        return DataPipeDecoratorMetaData(target=meta_type,
                                         selector=getattr(meta_type, DATAPIPE_DECORATOR_SELECTOR_KEY, ""),
                                         type=DecoratorMetaDataType.DATAPIPE)
    else:
        raise Exception(meta_type.__name__ + " is not a @DataPipe")


def scanServiceMetaData(meta_type: Type[Any]) -> ServiceDecoratorMetaData:
    if isDecorated(meta_type, INJECTABLE_WATERMARK):
        return ServiceDecoratorMetaData(target=meta_type,
                                        scope=getattr(meta_type, INJECTABLE_DECORATOR_INJECTION_SCOPE_KEY,
                                                      InjectionScope.DEFAULT))
    else:
        raise Exception(meta_type.__name__ + " is not a @Service")


def scanTaskMetaData(meta_type: Type[Any]) -> TaskDecoratorMetaData:
    if isDecorated(meta_type, TASK_WATERMARK):
        return TaskDecoratorMetaData(target=meta_type, template=getattr(meta_type, TASK_DECORATOR_TEMPLATE_URI_KEY, ""),
                                     type=DecoratorMetaDataType.TASK)
    else:
        raise Exception(meta_type.__name__ + " is not a @Task")


def scan_class_injects(cls: Type[Any], cls_method: Callable = None) -> Dict[str, InjectMetaData]:
    cls_method = cls_method if cls_method is not None else cls.__init__
    injects: Dict[str, InjectMetaData] = getattr(cls_method, INJECT_FN_DEPENDENCY_KEY, {})
    parameters: Dict[str, Parameter] = signature(cls_method).parameters
    for parameter_name, parameter in parameters.items():
        if parameter_name in ['self', 'args', 'kwargs']:
            continue
        if injects.get(parameter_name) is None:
            # If no InjectMetaData is provided, fall back to the type annotation
            if parameter.annotation is not Parameter.empty:
                injects[parameter_name] = InjectMetaData(token=parameter.annotation, scope=InjectionScope.DEFAULT,
                                                         optional=False)
            elif cls_method == cls.__init__:
                raise ValueError(
                    f"Cannot scan inject metadata for argument '{parameter_name}' in class '{cls.__name__}'")
            else:
                raise ValueError(
                    f"Cannot scan inject metadata for argument '{parameter_name}' in method '{cls_method.__name__}' in class '{cls.__name__}'")

    return injects


def scan_factory_injects(meta_data: FactoryProviderMetaData) -> Dict[str, InjectMetaData]:
    injects: Dict[str, InjectMetaData] = getattr(meta_data.use_factory, INJECT_FN_DEPENDENCY_KEY, {})
    parameters: Dict[str, Parameter] = signature(meta_data.use_factory).parameters
    for parameter_name, parameter in parameters.items():

        if injects.get(parameter_name) is None:
            # If no InjectMetaData is provided, fall back to the type annotation
            if parameter.annotation is not Parameter.empty:
                injects[parameter_name] = InjectMetaData(token=parameter.annotation, scope=InjectionScope.DEFAULT,
                                                         optional=False)
            else:
                raise ValueError(
                    f"Cannot scan inject metadata for argument '{parameter_name}' in factory provider '{meta_data.use_factory.__name__}'")

    return injects


def scan_class_options(cls: Type) -> Dict[str, Option]:
    return getattr(cls, OPTION_DECORATOR_KEY, {})
