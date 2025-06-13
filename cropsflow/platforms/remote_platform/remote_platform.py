import threading
from typing import Type, Any

import uvicorn
from fastapi import FastAPI

from core.application import Application
from cropsflow.data import DataModule
from cropsflow.events import EventsModule
from cropsflow.monitoring import MonitoringModule
from cropsflow.orchestrator import OrchestratorModule
from cropsflow.platforms import ApplicationPlatform
from cropsflow.router import RouterModule
from .platform_options import PlatformOptions
from .routes import get_api_router


class RemoteApplicationPlatform(ApplicationPlatform):
    __server_thread: threading.Thread

    async def start(self, module: Type[Any], options: PlatformOptions = PlatformOptions(),
                    args: list[str] = []) -> Application:
        await self.init(module, options=options,
                        overrides=[RouterModule, OrchestratorModule, MonitoringModule, EventsModule, DataModule])
        self.__server_thread = threading.Thread(target=self.__start_server, name='CropsFlow Gateway Platform',
                                                args=[options], daemon=False)
        self.__server_thread.start()
        print(f"CropsFlow server is running on http://{'localhost'}:{8000}")

    def __start_server(self, options: PlatformOptions) -> None:
        app = FastAPI(debug=True, title='CropsFlow Gateway API')
        app.include_router(prefix='/api', router=get_api_router(application=self.application))
        uvicorn.run(app, host="127.0.0.1", port=8000)
        return self.application

    async def shutdown(self):
        await uvicorn.Server.shutdown()


CropsFlowRemote = RemoteApplicationPlatform()
