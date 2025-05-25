from http import HTTPStatus

from fastapi import APIRouter

from cropsflow.common import InjectionScope
from cropsflow.common import service, inject
from .response import HttpErrorResponse, SuccessResponse


@service(scope=InjectionScope.DEFAULT)
class Router(APIRouter):

    @inject(arg_name='prefix', optional=True)
    def __init__(self, prefix: str = '/'):
        super().__init__(prefix=prefix)

    def use(self, path: str, router: 'Router'):
        if path.strip() in self.routes:
            self.include_router(prefix=path.strip(), router=router)

    @staticmethod
    def success(data: object, status: HTTPStatus = HTTPStatus.OK) -> SuccessResponse:
        return SuccessResponse(data=data, status=status)

    @staticmethod
    def error(error: Exception | str, status: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR) -> HttpErrorResponse:
        return HttpErrorResponse(error=error, status=status)
