from typing import List, Any, Union, Type, Callable, ForwardRef

from common.schemas.docorator_metadata import DecoratorMetaData
from common.utils import InjectionToken


class ProviderMetaData:
    provide: InjectionToken


class ClassProviderMetaData(ProviderMetaData):
    useClass: Type


class FactoryProviderMetaData(ProviderMetaData):
    useFactory: Callable


class ValueProviderMetaData(ProviderMetaData):
    useValue: Any


ProviderDef = Union[str, Type, ProviderMetaData]


class ModuleWithProviders:
    providers: List[ProviderDef]
    module: Type[Any]


ModuleDef = Union[ForwardRef, Type[Any], ModuleWithProviders, Callable]
ExportDef = Union[str, Type[Any]]


class ModuleDecoratorMetaData(DecoratorMetaData):
    declarations: [Type[Any]] = []
    imports: List[ModuleDef] = []
    providers: List[ProviderDef] = []
    exports: List[ExportDef] = []

    def __init__(self, declarations: List[Type[Any]] = [], imports: List[ModuleDef] = [],
                 providers: List[ProviderDef] = [], exports: List[ExportDef] = []):
        self.declarations = declarations
        self.imports = imports
        self.providers = providers
        self.exports = exports
