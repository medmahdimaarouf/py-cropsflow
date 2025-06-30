import threading
import traceback
from typing import Type, Any
from urllib.request import Request

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from setproctitle import setproctitle
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from cropsflow.core.application import Application
from cropsflow.data import DataModule
from cropsflow.events import EventsModule
from cropsflow.monitoring import MonitoringModule
from cropsflow.orchestrator import OrchestratorModule
from cropsflow.platforms import ApplicationPlatform
from cropsflow.router import RouterModule, Router
from .platform_options import PlatformOptions
from .routes import get_api_router


class RemoteApplicationPlatform(ApplicationPlatform):
    __server: uvicorn.Server | None = None
    __server_thread: threading.Thread | None = None

    async def start(self,
                    module: Type[Any],
                    port: int,
                    allow_origins: list = [],
                    log_level: str = 'info',
                    args: list[str] = []
                    ) -> Application:
        try:
            setproctitle("CropsFlow application")
            options = PlatformOptions(port=port, allow_origins=allow_origins)
            overrides: list = [RouterModule, OrchestratorModule, MonitoringModule, EventsModule, DataModule]
            await self.init(module, options=options, overrides=overrides)
            await self.__start_server_thread(options)
        except Exception as e:
            print(f"[start] Error: {e.__str__()}")
            traceback.print_exception(e)

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
        app.exception_handler(RequestValidationError)

        @app.exception_handler(RequestValidationError)
        async def validation_exception_handler(request: Request, exc: RequestValidationError):
            return JSONResponse(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                content=Router.error(error=exc, status=HTTP_422_UNPROCESSABLE_ENTITY).__dict__
            )

        config = uvicorn.Config(app=app, host="localhost", port=options.port, log_level="info")
        self.__server = uvicorn.Server(config)
        await self.__server.serve()

    async def shutdown(self):
        if self.__server:
            await self.__server.shutdown()


CropsFlowRemote = RemoteApplicationPlatform()
