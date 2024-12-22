from typing import Optional, Union, Any

from ..abstracts import DataModel

Number = Union[float, int]


class StringDataModel(DataModel[Number]):

    def serialize(self) -> Optional[Any]:
        return self.value
