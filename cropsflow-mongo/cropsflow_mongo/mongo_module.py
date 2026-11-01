from cropsflow.common import inject, ValueProviderMetaData, Init, DynamicModule, ExistsProvider
from cropsflow.common.decorators import module
from cropsflow.data import DataSource, DataSourcesRegister

from .consts import MONGO_MODULE_DBNAME
from .consts import MONGO_MODULE_URI
from .mongo_datasource import MongoDataSource
from .pipes import MongoDataSetInsertPipe
from .actions import MongoDataSetExistsAction, MongoCreateDataSetAction, MongoDataSetNotExistsAction


@module(
    declarations=[
        MongoDataSetExistsAction,
        MongoCreateDataSetAction,
        MongoDataSetNotExistsAction,
        MongoDataSetInsertPipe
    ],
    providers=[
        MongoDataSource,
        ExistsProvider(provide=DataSource, use_exists=MongoDataSource)
    ],
    exports=[
        MongoDataSource,
        MongoDataSetExistsAction,
        MongoCreateDataSetAction,
        MongoDataSetNotExistsAction,
        MongoDataSetInsertPipe
    ]
)
class MongoModule(Init):

    @staticmethod
    def register(uri: str, db_name: str, is_global: bool = False):
        database_uri_provider = ValueProviderMetaData(provide=MONGO_MODULE_URI, use_value=uri)
        database_db_provider = ValueProviderMetaData(provide=MONGO_MODULE_DBNAME, use_value=db_name)
        return DynamicModule(module=MongoModule, providers=[database_uri_provider, database_db_provider], is_global=is_global)

    @inject(arg_name='uri', token=MONGO_MODULE_URI)
    @inject(arg_name='db', token=MONGO_MODULE_DBNAME)
    @inject(arg_name='register', token=DataSourcesRegister, optional=True)
    async def init(self, uri: str, mongo_data_source: MongoDataSource, db: str, register: DataSourcesRegister) -> None:
        register.register(source_name='mongo-data-source', source=mongo_data_source)
        mongo_data_source.connect(uri=uri, db=db)
