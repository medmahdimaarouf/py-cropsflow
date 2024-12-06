from core.injector.container import Container
from common.decorators import *
from common.utils import stringify_injection_token
from .resolve_status import ResolveStatus
from ..exceptions import CircularDependenciesException

T = TypeVar('T')


class Injector(Generic[T]):
    instance: T = None
    container: Container
    resolve_status: ResolveStatus = ResolveStatus.NONE

    def __init__(self, container: Container):
        self.container = container
        self.resolve_status = ResolveStatus.NONE if self.container.metadata is not None else ResolveStatus.RESOLVED

    def resolve(self, token: InjectionToken = None, scope: InjectionScope = None) -> T:
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
            return self.container.get(token).resolve(token)

    def resolve_instance(self, meta_data: DecoratorMetaData) -> T:
        instance = None
        if isinstance(meta_data, ProviderMetaData):
            if isinstance(meta_data, ClassProviderMetaData):
                instance = self.resolve_class_provider(meta_data)
            elif isinstance(meta_data, FactoryProviderMetaData):
                instance = self.resolve_factory_provider(meta_data)
            elif isinstance(meta_data, ValueProviderMetaData):
                instance = meta_data.useValue
            else:
                raise Exception("Unknown provider metadata type" + str(meta_data.__class__.__name__))
        else:
            instance = self.resolve_injectable(meta_data)

        return instance

    def resolve_class_provider(self, class_provider: ClassProviderMetaData) -> T:
        try:
            pass
        except CircularDependenciesException as e:
            if self.resolve_status == ResolveStatus.PENDING:
                raise CircularDependenciesException(stringify_injection_token(class_provider), self.container.name)
            else:
                raise e

    def resolve_factory_provider(self, factory_provider: FactoryProviderMetaData) -> T:
        try:
            pass
        except CircularDependenciesException as e:
            if self.resolve_status == ResolveStatus.PENDING:
                raise CircularDependenciesException(stringify_injection_token(factory_provider.provide),
                                                    self.container.name)
            else:
                raise e

    def resolve_all(self, tokens: List[str]) -> Dict[str, Any]:
        pass


NULL_INJECTOR = Injector(Container(None))
