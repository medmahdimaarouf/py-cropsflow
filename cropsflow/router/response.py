from http import HTTPStatus


class HttpResponse:
    success: bool = False
    status: HTTPStatus = HTTPStatus.OK

    def __init__(self, success: bool, status: HTTPStatus = HTTPStatus.OK):
        self.success = success
        self.status = status


class HttpErrorResponse(HttpResponse):
    error: str

    def __init__(self, error: Exception | str, status: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR):
        super().__init__(success=False, status=status)
        self.error = error.__cause__.__str__() if isinstance(error, Exception) else error


class SuccessResponse(HttpResponse):
    data: object = {}

    def __init__(self, data: object, status: HTTPStatus = HTTPStatus.OK):
        super().__init__(success=True, status=status)
        self.data = data or {}
