import threading
from typing import Type, Any

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from cropsflow.core.application import Application
from cropsflow.data import DataModule
from cropsflow.events import EventsModule
from cropsflow.monitoring import MonitoringModule
from cropsflow.orchestrator import OrchestratorModule
from cropsflow.platforms import ApplicationPlatform
from cropsflow.router import RouterModule
from .platform_options import PlatformOptions
from .routes import get_api_router


class RemoteApplicationPlatform(ApplicationPlatform):
    __server: uvicorn.Server | None = None
    __server_thread: threading.Thread | None = None

    async def start(self,
                    module: Type[Any],
                    port: int,
                    allow_origins: list = [],
                    args: list[str] = []
                    ) -> Application:
        try:
            options = PlatformOptions(port=port, allow_origins=allow_origins)
            overrides: list = [RouterModule, OrchestratorModule, MonitoringModule, EventsModule, DataModule]
            await self.init(module, options=options, overrides=overrides)
            await self.__start_server_thread(options)
        except Exception as e:
            print(f"[start] Error: {e.__str__()}")

    async def __start_server_thread(self, options: PlatformOptions) -> None:
        app = FastAPI(debug=True, title='CropsFlow Gateway API')
        app.add_middleware(
            CORSMiddleware,
            allow_origins=options.allow_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        app.include_router(prefix='/api', router=get_api_router(application=self.application))

        config = uvicorn.Config(app=app, host="localhost", port=options.port, log_level="info")
        self.__server = uvicorn.Server(config)
        await self.__server.serve()

    async def shutdown(self):
        if self.__server:
            await self.__server.shutdown()


CropsFlowRemote = RemoteApplicationPlatform()
