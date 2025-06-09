import asyncio
import uuid

from .abstracts.data_source import DataSource
from cropsflow.common.decorators import service, InjectionScope


@service(scope=InjectionScope.DEFAULT)
class DataSourcesRegister:
    sources: dict[str, DataSource] = {}

    def register(self, source_name: str, source: DataSource) -> DataSource:
        url_name = source_name.strip()
        while url_name.count('  '):
            url_name.replace('  ', ' ')
        while url_name.count(' '):
            url_name.replace(' ', '-')

        counter: int = 1 if url_name in self.sources else 0
        while f"{url_name}-{counter}" in self.sources:
            counter = counter + 1
        self.sources.setdefault(f"{url_name}-{counter}", source)
        return source

    def remove(self, source_name: str) -> None:
        ds: DataSource = self.sources.pop(source_name.strip())
        if ds.connected:
            asyncio.run(ds.disconnect())
