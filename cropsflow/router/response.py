from http import HTTPStatus
from typing import final


class HttpResponse:
    def __init__(self, success: bool, status: HTTPStatus = HTTPStatus.OK):
        super().__init__()
        self.success: bool = success
        self.status: HTTPStatus = status


@final
class HttpErrorResponse(HttpResponse):
    def __init__(self, error: Exception | str, status: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR):
        super().__init__(success=False, status=status)
        self.error = error.__cause__.__str__() if isinstance(error, Exception) else error


@final
class SuccessResponse(HttpResponse):
    def __init__(self, data: object, status: HTTPStatus = HTTPStatus.OK):
        super().__init__(success=True, status=status)
        self.data: object = data
