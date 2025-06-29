from typing import Optional

from cropsflow.common import service, InjectionScope
from .monitor import Monitor


@service(scope=InjectionScope.DEFAULT)
class MonitorsManager:
    def __init__(self):
        self.__monitors: dict[str, Monitor] = {}

    def register(self, name: str, monitor: Monitor, description: str = None) -> None:
        monitor_id: str = name.strip().lower().replace('  ', ' ').replace(' ', '-')
        if monitor_id not in self.__monitors:
            setattr(monitor, '__name', name.strip())
            setattr(monitor, '__description', description)
            setattr(monitor, '__id', monitor_id)
            return self.__monitors.setdefault(monitor.id, monitor)

    def get(self, monitor_id: str) -> Optional[Monitor]:
        return self.__monitors.get(monitor_id.strip(), None)
