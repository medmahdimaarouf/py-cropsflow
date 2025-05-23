from typing import Generic

from cropsflow.common.decorators import *
from cropsflow.common.utils import stringify_injection_token
from ..abstracts import BaseInjector, ResolveStatus
from ..abstracts.container import BaseContainer
from ..exceptions import CircularDependenciesException
from ..scanner.metadata_scanner import scan_factory_injects, scan_class_injects

T = TypeVar('T')


class NullInjector(BaseInjector):
    resolve_status = ResolveStatus.NONE

    def resolve(self, token: InjectionToken = None, scope: InjectionScope = None, optional: bool = False) -> T:
        if optional:
            return None
        else:
            raise Exception(f'Null injector found for {stringify_injection_token(token)}')


NULL_INJECTOR = NullInjector()


class Injector(Generic[T], BaseInjector[T]):

    def __init__(self, container: BaseContainer = None, instance: T = None):
        self.instance = instance
        self.container = container
        self.resolve_status = ResolveStatus.NONE if not self.instance else ResolveStatus.RESOLVED

    def resolve(self, token: InjectionToken = None, scope: InjectionScope = None, optional: bool = False) -> T:
        if token is None:
            if self.resolve_status == ResolveStatus.NONE:
                self.resolve_status = ResolveStatus.PENDING
                if self.container.metadata is None:
                    self.instance = None
                else:
                    self.instance = self.resolve_instance(self.container.metadata)
                self.resolve_status = ResolveStatus.RESOLVED
            return self.instance
        else:
            injector = self.container.get(token=token)
            if injector == NULL_INJECTOR:
                if optional:
                    return None
                else:
                    return injector.resolve(token)
            else:
                return injector.resolve(scope=scope, optional=optional)

    def resolve_instance(self, meta_data: Union[DecoratorMetaData, ProviderMetaData]) -> T:
        if isinstance(meta_data, ProviderMetaData):
            return self.resolve_provider(meta_data)
        else:
            return self.resolve_class(meta_data.target)

    def resolve_provider(self, meta_data: ProviderMetaData):
        if isinstance(meta_data, ClassProviderMetaData):
            return self.resolve_class(meta_data.useClass)
        elif isinstance(meta_data, FactoryProviderMetaData):
            return self.resolve_factory_provider(meta_data)
        elif isinstance(meta_data, ValueProviderMetaData):
            return meta_data.use_value
        elif isinstance(meta_data, ExistsProvider):
            return self.resolve(meta_data.use_exists)
        else:
            raise Exception("Unknown provider metadata " + str(meta_data.__class__.__name__))

    def resolve_class(self, cls: Type[Any]) -> Any:
        try:
            # Get the constructor (__init__) signature
            injects: Dict[str, InjectMetaData] = scan_class_injects(cls=cls)
            resolved_parameters: Dict[str, Any] = {}
            for param_name, inject_meta_data in injects.items():
                resolved_parameters[param_name] = self.resolve(token=inject_meta_data.token,
                                                               scope=inject_meta_data.scope,
                                                               optional=inject_meta_data.optional)

            return cls(**resolved_parameters)
        except CircularDependenciesException as e:
            if self.resolve_status == ResolveStatus.PENDING:
                raise CircularDependenciesException(stringify_injection_token(cls), self.container.name)
            else:
                raise e

    def resolve_factory_provider(self, factory_provider: FactoryProviderMetaData) -> T:
        try:
            injects: Dict[str, InjectMetaData] = scan_factory_injects(factory_provider)
            resolved_parameters: Dict[str, Any] = {}
            for param_name, inject_meta_data in injects.items():
                resolved_parameters[param_name] = self.resolve(token=inject_meta_data.token,
                                                               scope=inject_meta_data.scope,
                                                               optional=inject_meta_data.optional)
            return factory_provider.use_factory(**resolved_parameters)
        except CircularDependenciesException as e:
            if self.resolve_status == ResolveStatus.PENDING:
                raise CircularDependenciesException(stringify_injection_token(factory_provider.provide),
                                                    self.container.name)
            else:
                raise e

    def resolve_class_method_deps(self, cls: Type, method: Callable) -> Dict[str, Any]:
        try:
            injects: Dict[str, InjectMetaData] = scan_class_injects(cls=cls, cls_method=method)
            resolved_parameters: Dict[str, Any] = {}
            for param_name, inject_meta_data in injects.items():
                resolved_parameters[param_name] = self.resolve(token=inject_meta_data.token,
                                                               scope=inject_meta_data.scope,
                                                               optional=inject_meta_data.optional)
            return resolved_parameters
        except CircularDependenciesException as e:
            if self.resolve_status == ResolveStatus.PENDING:
                raise CircularDependenciesException(stringify_injection_token(cls), self.container.name)
            else:
                raise e
