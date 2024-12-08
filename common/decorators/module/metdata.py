from typing import List, Any, Union, Type, Callable

from common.schemas.docorator_metadata import DecoratorMetaData
from common.utils import InjectionToken


class ProviderMetaData:
    provide: InjectionToken

    def __init__(self, provide: InjectionToken):
        self.provide = provide


class ClassProviderMetaData(ProviderMetaData):
    useClass: Type

    def __init__(self, provide: InjectionToken, useClass: Type):
        super().__init__(provide=provide)
        self.useClass = useClass


class FactoryProviderMetaData(ProviderMetaData):
    useFactory: Callable

    def __init__(self, provide: InjectionToken, useFactory: Callable):
        super().__init__(provide=provide)
        self.useFactory = useFactory


class ValueProviderMetaData(ProviderMetaData):
    useValue: Any

    def __init__(self, provide: InjectionToken, useValue: Any):
        super().__init__(provide=provide)
        self.useValue = useValue


ProviderDef = Union[Type, ProviderMetaData]


class DynamicModule:
    providers: List[ProviderDef]
    module: Type[Any]
    is_global: bool

    def __init__(self, module: Type[Any], provider: Type[ProviderDef], is_global: bool):
        self.module = module
        self.provider = provider
        self.is_global = is_global


ModuleDef = Union[Type[Any], DynamicModule, Callable]
ExportDef = Union[str, Type[Any]]


class ModuleDecoratorMetaData(DecoratorMetaData):
    declarations: [Type[Any]] = []
    imports: List[ModuleDef] = []
    providers: List[ProviderDef] = []
    exports: List[ExportDef] = []

    def __init__(self, target: Type[Any], declarations: List[Type[Any]] = [], imports: List[ModuleDef] = [],
                 providers: List[ProviderDef] = [], exports: List[ExportDef] = []):
        self.target = target
        self.declarations = declarations
        self.imports = imports
        self.providers = providers
        self.exports = exports
