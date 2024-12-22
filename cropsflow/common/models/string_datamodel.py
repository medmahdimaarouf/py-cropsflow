from typing import Optional, Any

from ..abstracts import DataModel


class StringDataModel(DataModel[str]):

    def serialize(self) -> Optional[Any]:
        return self.value
