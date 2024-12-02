from enum import Enum


class DecoratorMetaDataType(Enum):
    CLASS = "class"
    INJECTABLE = "service"
    MODULE = "module"
    FACTORY = "factory"
    DATAPIPE = "datapipe"
    ACTION = "action"
    TASK = "task"
    INJECT = "inject"
