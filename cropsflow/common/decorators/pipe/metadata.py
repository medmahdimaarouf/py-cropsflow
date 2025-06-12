"""
Defines metadata for a DataPipe decorator, which is used to mark
a class as a data transformation component with a specific selector.
"""

from dataclasses import dataclass, field
from typing import Type, Any

from ...schemas import DecoratorMetaData, DecoratorMetaDataType


@dataclass
class DataPipeDecoratorMetaData(DecoratorMetaData):
    """
    Metadata structure for classes decorated as DataPipes.

    Attributes:
        selector (str): The unique identifier for the datapipe.
        type (DecoratorMetaDataType): The type of the decorator, fixed to DATAPIPE.
    """
    selector: str = field(default_factory=str)
    type: DecoratorMetaDataType = DecoratorMetaDataType.DATAPIPE
