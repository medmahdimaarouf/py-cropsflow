from typing import Type, Any

from cropsflow.data import DataModule
from cropsflow.events import EventsModule
from cropsflow.monitoring import MonitoringModule
from cropsflow.router import RouterModule

from cropsflow.core.application import Application
from cropsflow.core.application_options import ApplicationOptions
from .application_platform import ApplicationPlatform
from ..orchestrator import OrchestratorModule


class StaticPlatform(ApplicationPlatform):

    async def start(self, t: Type[Any], options: ApplicationOptions = ApplicationOptions(),
                    args: list[str] = []) -> Application:
        return await self.init(t, options=options,
                               overrides=[RouterModule, OrchestratorModule, MonitoringModule, EventsModule, DataModule])


CropsFlow = StaticPlatform()
