from typing import Dict, Any

from cropsflow.common import action, option, Action, TaskContext

from ..dataset import MongoDataSet
from ..mongo_datasource import MongoDataSource


@action(selector='mongo-not-exists-dataset-action', auto_next=False)
@option(key='dataset', required=True)
class MongoDataSetNotExistsAction(Action):
    mongo_data_source: MongoDataSource = None

    def __init__(self, mongo_data_source: MongoDataSource):
        self.mongo_data_source = mongo_data_source

    async def run(self, context: TaskContext, options: Dict[str, Any] = {}) -> TaskContext:
        dataset_name: str = options.get('dataset').strip()
        mongo_dataset: MongoDataSet = await self.mongo_data_source.get_dataset(name=dataset_name)
        if mongo_dataset is None:
            await self.next(context=context)
        return context
