from typing import Dict, Any

from cropsflow.common import inject, pipe, option, Pipe, TaskContext

from ..dataset import MongoDataSet
from ..mongo_datasource import MongoDataSource


@pipe(selector='mongo-dataset-insert-pipe')
@option(key='dataset', required=True)
class MongoDataSetInsertPipe(Pipe):
    def __init__(self, mongo_data_source: MongoDataSource):
        self.mongo_data_source = mongo_data_source

    def transform(self, data: any = None, options: Dict[str, Any] = None) -> None:
        mongo_dataset: MongoDataSet = self.mongo_data_source.get_dataset(options.get('dataset'))
        mongo_dataset.save(data=data if isinstance(data, dict) else {'data': data})
        self._data = data
