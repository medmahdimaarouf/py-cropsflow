from typing import Optional


class UIDataModel:
    """
    Abstract base class for a generic metric.
    """

    @property
    def name(self) -> Optional[str]:
        return getattr(self, '__name', None)

    @property
    def description(self) -> Optional[str]:
        return getattr(self, '__description')

    @property
    def id(self) -> Optional[str]:
        return getattr(self, '__id')
