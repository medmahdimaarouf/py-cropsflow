from enum import Enum

import requests
from cropsflow.common import service, InjectionScope
from requests import Response


class HttpRequestMethod(Enum):
    GET = 'GET',
    POST = "POST",
    PUT = 'PUT',
    DELETE = 'DELETE'
    PATCH = 'PATCH'


@service(scope=InjectionScope.TRANSIENT)
class HttpRequestsService:

    @staticmethod
    def get_mimic_browser_headers(url: str):
        return {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            ),
            "Accept": (
                "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
            ),
            "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": url,
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }

    @classmethod
    def get(cls, url: str, params: dict[str, any] = {}, **args) -> Response:
        response = cls.request(method=HttpRequestMethod.GET, url=url, params=params, **args)
        response.raise_for_status()
        response.close()
        return response

    @classmethod
    def post(cls, url: str, data: any, **args) -> Response:
        response = cls.request(method=HttpRequestMethod.POST, url=url, data=data, **args)
        response.raise_for_status()
        response.close()
        return response

    @classmethod
    def put(cls, url: str, data: any, params: dict[str, any] = {}, **args) -> Response:
        response = cls.request(method=HttpRequestMethod.PUT, url=url, data=data, params=params, **args)
        response.raise_for_status()
        response.close()
        return response

    @classmethod
    def delete(cls, url: str, params: dict[str, any] = {}, **args) -> Response:
        response = cls.request(method=HttpRequestMethod.DELETE, url=url, params=params, **args)
        response.raise_for_status()
        response.close()
        return response

    @classmethod
    def patch(cls, url: str, params: dict[str, any] = {}, **args) -> Response:
        response = cls.request(method=HttpRequestMethod.PATCH, url=url, params=params, **args)
        response.raise_for_status()
        response.close()
        return response

    @classmethod
    def request(cls,
                method: HttpRequestMethod,
                url: str,
                data: any = None,
                params: dict[str, any] = {},
                headers: dict[str, str] = {},
                cookies: dict[str, str] = {},
                allow_redirects: bool = True,
                timeout: int = None
                ) -> Response:
        return requests.request(
            method=method.name,
            url=url,
            data=data,
            params=params,
            headers=headers,
            cookies=cookies,
            allow_redirects=allow_redirects,
            timeout=timeout
        )
