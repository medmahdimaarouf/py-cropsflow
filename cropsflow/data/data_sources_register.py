import uuid

from .abstracts.data_source import DataSource
from cropsflow.common.decorators import service, InjectionScope


@service(scope=InjectionScope.DEFAULT)
class DataSourcesRegister:
    sources: dict[str, DataSource] = []

    def register(self, source: DataSource) -> DataSource:
        self.sources.setdefault(uuid.uuid4(), source)
        return source

    def remove(self, source_id: str) -> None:
        self.sources.pop(source_id.strip())
