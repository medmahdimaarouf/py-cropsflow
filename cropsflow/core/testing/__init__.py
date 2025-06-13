from typing import List, Type, Any

from cropsflow.common.decorators.module import ModuleDef, ProviderDef, module
from ..application import Application
from ..injector import Injector


class CropsFlowTesting:
    @staticmethod
    async def create_test_module(declarations: List[Type[Any]] = [], imports: List[ModuleDef] = [],
                                 providers: List[ProviderDef] = []) -> Injector:
        @module(declarations=declarations, imports=imports, providers=providers)
        class TestModule:
            pass

        application: Application = Application()
        await application.bootstrap(module=TestModule)
        return application.get_module(meta_type=TestModule).injector
