import asyncio
import traceback
from functools import wraps
from http import HTTPStatus
from typing import Callable, Any, Type

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from cropsflow.common import InjectionScope
from cropsflow.common import service, inject
from .response import HttpErrorResponse, SuccessResponse, HttpResponse


@service(scope=InjectionScope.DEFAULT)
class Router(APIRouter):

    @inject(arg_name='prefix', token='router_prefix', optional=True)
    def __init__(self, prefix: str = ''):
        super().__init__(prefix=prefix or '')
        self._exception_wrappers: dict[Callable, list[Exception]] = {}

    def use(self, path: str, router: 'Router'):
        if path.strip() in self.routes:
            self.include_router(prefix=path.strip(), router=router)

    @staticmethod
    def success(data: object, status: HTTPStatus = HTTPStatus.OK) -> SuccessResponse:
        return SuccessResponse(data=data, status=status)

    @staticmethod
    def error(error: Exception | str, status: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR) -> HttpErrorResponse:
        return HttpErrorResponse(error=error.__class__.__name__ if isinstance(error, Exception) else error,
                                 status=status)

    def handle_exception(self, exception_type: Type[Exception], status: int):
        def decorator(func: Callable):
            # Store registered exceptions for this function
            self._exception_wrappers.setdefault(func, []).append(exception_type)

            @wraps(func)
            async def wrapper(*args, **kwargs):
                try:
                    response: HttpResponse = None
                    if asyncio.iscoroutinefunction(func):
                        response = await func(*args, **kwargs)
                    else:
                        response = func(*args, **kwargs)
                    if isinstance(response, HttpErrorResponse):
                        return JSONResponse(content=response.__dict__, status_code=response.status)
                    elif isinstance(response, SuccessResponse):
                        return JSONResponse(content=response.__dict__, status_code=response.status)
                    else:
                        return JSONResponse(content=response.__dict__, status_code=200)

                except tuple(self._exception_wrappers[func]) as e:
                    traceback.print_exception(e)
                    return JSONResponse(content=self.error(error=e, status=status).__dict__, status_code=status)
                except Exception as e:
                    traceback.print_exception(e)
                    return JSONResponse(content=self.error(error=e, status=status).__dict__)

            return wrapper

        return decorator
