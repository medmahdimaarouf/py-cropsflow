from typing import Type, Any, List
from common.constants import *
from common.decorators import ModuleDecoratorMetaData, ActionDecoratorMetaData, DataPipeDecoratorMetaData, \
    ServiceDecoratorMetaData, TaskDecoratorMetaData


def isDecorated(meta_type: Type[Any], watermark: str) -> bool:
    return watermark in getattr(meta_type, DECORATOR_WATERMARKS, [])


def getDecorators(meta_type: Type[Any]) -> List[str]:
    return getattr(meta_type, DECORATOR_WATERMARKS, [])


def scanModuleMetaData(meta_type: Type[Any]) -> ModuleDecoratorMetaData:
    if isDecorated(meta_type, MODULE_WATERMARK):
        return ModuleDecoratorMetaData(
            declarations=getattr(meta_type, MODULE_DECORATOR_DECLARATIONS_KEY, []),
            imports=getattr(meta_type, MODULE_DECORATOR_IMPORTS_KEY, []),
            providers=getattr(meta_type, MODULE_DECORATOR_PROVIDERS_KEY, []),
            exports=getattr(meta_type, MODULE_DECORATOR_EXPORTS_KEY, [])
        )
    else:
        raise Exception(meta_type.__name__ + " is not a @Module")


def scanActionMetaData(meta_type: Type[Any]) -> ActionDecoratorMetaData:
    if isDecorated(meta_type, ACTION_WATERMARK):
        return ActionDecoratorMetaData(selector=getattr(meta_type, ACTION_DECORATOR_SELECTOR_KEY, ""))
    else:
        raise Exception(meta_type.__name__ + " is not an @Action")


def scanDataPipeMetaData(meta_type: Type[Any]) -> DataPipeDecoratorMetaData:
    if isDecorated(meta_type, PIPE_WATERMARK):
        return DataPipeDecoratorMetaData(selector=getattr(meta_type, DATAPIPE_DECORATOR_SELECTOR_KEY, ""))
    else:
        raise Exception(meta_type.__name__ + " is not a @DataPipe")


def scanServiceMetaData(meta_type: Type[Any]) -> ServiceDecoratorMetaData:
    if isDecorated(meta_type, INJECTABLE_WATERMARK):
        return ServiceDecoratorMetaData(selector=getattr(meta_type, INJECTABLE_DECORATOR_PROVIDER_HOST_KEY, ""))
    else:
        raise Exception(meta_type.__name__ + " is not a @Service")


def scanTaskMetaData(meta_type: Type[Any]) -> TaskDecoratorMetaData:
    if isDecorated(meta_type, TASK_WATERMARK):
        return TaskDecoratorMetaData(selector=getattr(meta_type, TASK_DECORATOR_TEMPLATE_URI_KEY, ""))
    else:
        raise Exception(meta_type.__name__ + " is not a @Task")
