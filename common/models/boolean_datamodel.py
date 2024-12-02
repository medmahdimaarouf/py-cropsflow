from typing import Optional, Any

from common.abstracts import DataModel


class BooleanDataModel(DataModel[bool]):

    def serialize(self) -> Optional[Any]:
        return self.value
