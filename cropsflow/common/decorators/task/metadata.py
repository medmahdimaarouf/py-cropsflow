"""
Defines metadata for the Task decorator, used to annotate classes that represent task templates.
"""

from dataclasses import dataclass, field

from ...schemas import DecoratorMetaData, DecoratorMetaDataType


@dataclass
class TaskDecoratorMetaData(DecoratorMetaData):
    """
    Metadata class for task decorators.

    Attributes:
        template (str): A string identifier referencing the task template.
        type (DecoratorMetaDataType): Constant indicating this metadata is for a task.
    """
    template: str = field(default_factory=str)
    built_in: bool = field(default=False)
    type: DecoratorMetaDataType = DecoratorMetaDataType.TASK
