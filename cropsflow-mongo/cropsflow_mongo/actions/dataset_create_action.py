from typing import Dict, Any

from cropsflow.common import action, option, Action, TaskContext

from ..dataset import MongoDataSet
from ..mongo_datasource import MongoDataSource


@action(selector='mongo-create-dataset-action')
@option(key='dataset', required=True)
@option(key='drop', required=False, default=True)
class MongoCreateDataSetAction(Action):
    mongo_data_source: MongoDataSource = None

    def __init__(self, mongo_data_source: MongoDataSource):
        self.mongo_data_source = mongo_data_source

    async def run(self, context: TaskContext, options: Dict[str, Any] = {}) -> TaskContext:
        dataset_name: str = options.get('dataset').strip()
        drop_data_set: bool = options.get('drop', True)
        mongo_dataset: MongoDataSet = self.mongo_data_source.get_dataset(name=dataset_name)
        if mongo_dataset is None:
            self.mongo_data_source.create_dataset(name=dataset_name)
        elif drop_data_set:
            self.mongo_data_source.delete_dataset(name=dataset_name)
            self.mongo_data_source.create_dataset(name=dataset_name)
        return context
