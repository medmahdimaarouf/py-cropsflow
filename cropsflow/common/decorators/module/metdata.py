"""
Defines metadata classes used for configuring dependency injection in modules,
including support for class, factory, and value providers, as well as dynamic modules.

This module is designed to support a modular DI system and includes data structures
that facilitate metadata collection during module declaration and registration.
"""

from dataclasses import dataclass, field
from typing import List, Any, Union, Type, Callable

from cropsflow.common.schemas.docorator_metadata import DecoratorMetaData
from cropsflow.common.utils import InjectionToken


@dataclass
class ProviderMetaData:
    """Base metadata for providers with a token key."""
    provide: InjectionToken = field(default_factory=str)

    def __init__(self, provide: InjectionToken):
        self.provide = provide


@dataclass
class ClassProviderMetaData(ProviderMetaData):
    """Metadata for class-based providers."""
    useClass: Type[Any] = field(default_factory=object)

    def __init__(self, provide: InjectionToken, useClass: Type[Any]):
        super().__init__(provide=provide)
        self.useClass = useClass


@dataclass
class FactoryProviderMetaData(ProviderMetaData):
    """Metadata for factory-based providers."""
    use_factory: Callable = field(default_factory=lambda: None)

    def __init__(self, provide: InjectionToken, use_factory: Callable):
        super().__init__(provide=provide)
        self.use_factory = use_factory


@dataclass
class ValueProviderMetaData(ProviderMetaData):
    """Metadata for value-based providers."""
    use_value: Any = field(default=None)

    def __init__(self, provide: InjectionToken, use_value: Any):
        super().__init__(provide=provide)
        self.use_value = use_value


@dataclass
class ExistsProvider(ProviderMetaData):
    """Metadata for existing providers (aliases)."""
    use_exists: InjectionToken = field(default_factory=str)

    def __init__(self, provide: InjectionToken, use_exists: InjectionToken):
        super().__init__(provide=provide)
        self.use_exists = use_exists


ProviderDef = Union[Type[Any], ProviderMetaData]


@dataclass
class DynamicModule:
    """Represents a dynamic module with runtime-registered providers."""
    module: Type[Any] = field(default_factory=object)
    providers: List[ProviderDef] = field(default_factory=list)
    is_global: bool = field(default=False)

    def __init__(
            self,
            module: Type[Any],
            providers: List[ProviderDef],
            is_global: bool = False
    ):
        self.module = module
        self.providers = providers
        self.is_global = is_global


ModuleDef = Union[Type[Any], DynamicModule, Callable]


@dataclass
class ModuleDecoratorMetaData(DecoratorMetaData):
    """Metadata for the @Module decorator."""
    declarations: List[Type[Any]] = field(default_factory=list)
    imports: List[ModuleDef] = field(default_factory=list)
    providers: List[ProviderDef] = field(default_factory=list)
    exports: List[InjectionToken] = field(default_factory=list)

    def __init__(
            self,
            target: Type[Any],
            declarations: List[Type[Any]] = None,
            imports: List[ModuleDef] = None,
            providers: List[ProviderDef] = None,
            exports: List[InjectionToken] = None
    ):
        self.target = target
        self.declarations = declarations or []
        self.imports = imports or []
        self.providers = providers or []
        self.exports = exports or []