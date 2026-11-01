from dataclasses import dataclass

from cropsflow.common import TaskContext


@dataclass()
class HttpResponseTaskContext(TaskContext):
    def __init__(self, ok: bool, status_code: int, text: str, content: str, headers: dict = {}, cookies: dict = {}):
        self.ok = ok
        self.status_code = status_code
        self.text = text
        self.content = content
        self.headers = headers
        self.cookies = cookies


@dataclass()
class HttpJSONResponseTaskContext(HttpResponseTaskContext):
    data: any = None

    def __init__(self, data: any):
        self.data = data
