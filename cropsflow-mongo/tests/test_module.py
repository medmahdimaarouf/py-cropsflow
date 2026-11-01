import asyncio

from cropsflow.common.decorators import module
from cropsflow.common import CommonModule
from cropsflow_mongo import MongoModule
from tests.test_task import TestTask


@module(
    declarations=[
        TestTask
    ],
    imports=[
        CommonModule,
        MongoModule.register(uri='mongodb://localhost:27017', db_name='prx-automobile-tn')
    ],
)
class TestModule:
    def __init__(self):
        pass



