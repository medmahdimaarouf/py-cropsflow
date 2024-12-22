from dataclasses import dataclass, field
from typing import List, Any, Union, Type, Callable

from cropsflow.common.schemas.docorator_metadata import DecoratorMetaData
from cropsflow.common.utils import InjectionToken


@dataclass()
class ProviderMetaData:
    provide: InjectionToken = field(default_factory=str)

    def __init__(self, provide: InjectionToken):
        self.provide = provide


@dataclass()
class ClassProviderMetaData(ProviderMetaData):
    useClass: Type = field(default_factory=Type)

    def __init__(self, provide: InjectionToken, useClass: Type):
        super().__init__(provide=provide)
        self.useClass = useClass


@dataclass()
class FactoryProviderMetaData(ProviderMetaData):
    use_factory: Callable = field(default_factory=Callable)

    def __init__(self, provide: InjectionToken, use_factory: Callable):
        super().__init__(provide=provide)
        self.use_factory = use_factory


@dataclass()
class ValueProviderMetaData(ProviderMetaData):
    use_value: Any = field(default_factory=any)

    def __init__(self, provide: InjectionToken, use_value: Any):
        super().__init__(provide=provide)
        self.use_value = use_value


ProviderDef = Union[Type, ProviderMetaData]


@dataclass()
class DynamicModule:
    providers: List[ProviderDef] = field(default_factory=list)
    module: Type[Any] = field(default_factory=Type)
    is_global: bool = field(default_factory=bool)

    def __init__(self, module: Type[Any], provider: Type[ProviderDef], is_global: bool):
        self.module = module
        self.provider = provider
        self.is_global = is_global


ModuleDef = Union[Type[Any], DynamicModule, Callable]


@dataclass()
class ModuleDecoratorMetaData(DecoratorMetaData):
    declarations: [Type[Any]] = field(default_factory=list)
    imports: List[ModuleDef] = field(default_factory=list)
    providers: List[ProviderDef] = field(default_factory=list)
    exports: List[InjectionToken] = field(default_factory=list)

    def __init__(self, target: Type[Any], declarations: List[Type[Any]] = [], imports: List[ModuleDef] = [],
                 providers: List[ProviderDef] = [], exports: List[InjectionToken] = []):
        self.target = target
        self.declarations = declarations
        self.imports = imports
        self.providers = providers
        self.exports = exports
