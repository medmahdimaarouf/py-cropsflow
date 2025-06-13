from typing import List, Type, Any

from cropsflow.common.decorators.module import ModuleDef, ProviderDef, module
from cropsflow.common import InjectionScope
from ..application import Application

from ..injector import Injector
from ..scanner.dependency_scanner import DependenciesScanner


class CropsFlowTesting:
    @staticmethod
    async def create_test_module(self, declarations: List[Type[Any]] = [], imports: List[ModuleDef] = [],
                                 providers: List[ProviderDef] = []) -> Injector:
        @module(declarations=declarations, imports=imports, providers=providers)
        class TestModule:
            pass

        application: Application = Application()
        application.bootstrap(module=TestModule)
        return application.get_module(meta_type=TestModule).injector
