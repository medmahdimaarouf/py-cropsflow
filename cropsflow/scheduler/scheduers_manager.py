from typing import Optional

from cropsflow.common import InjectionScope, service
from .async_scheduler import AsyncScheduler
from .background_scheduler import BackgroundScheduler
from .base_scheduler import BaseScheduler


@service(InjectionScope.DEFAULT)
class SchedulersManager:
    def __init__(self):
        self.__schedulers = dict[str, BaseScheduler] = {}

    def create_async(self, name: str, description: str = None) -> Optional[AsyncScheduler]:
        scheduler_id: str = name.strip().lower().replace('  ', ' ').replace(' ', '-')
        scheduler: AsyncScheduler = AsyncScheduler()
        if scheduler_id not in self.__schedulers:
            setattr(scheduler, '__name', name.strip())
            setattr(scheduler, '__description', description)
            setattr(scheduler, '__id', scheduler_id)
            return self.__schedulers.setdefault(scheduler.id, scheduler)

    def create_background(self, name: str, description: str = None) -> Optional[AsyncScheduler]:
        scheduler_id: str = name.strip().lower().replace('  ', ' ').replace(' ', '-')
        scheduler: BackgroundScheduler = BackgroundScheduler()
        if scheduler_id not in self.__schedulers:
            setattr(scheduler, '__name', name.strip())
            setattr(scheduler, '__description', description)
            setattr(scheduler, '__id', scheduler_id)
            return self.__schedulers.setdefault(scheduler.id, scheduler)

    def get(self, scheduler_id: str) -> Optional[BaseScheduler]:
        return self.__schedulers.get(scheduler_id.strip(), None)
