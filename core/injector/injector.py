from inspect import Parameter

from common.decorators import *
from common.utils import stringify_injection_token
from ..abstracts import BaseInjector, ResolveStatus
from ..abstracts.base_container import BaseContainer
from ..exceptions import CircularDependenciesException

T = TypeVar('T')


class Injector(Generic[T], BaseInjector[T]):

    def __init__(self, container: BaseContainer = None, instance: T = None):
        self.container = container
        self.instance = instance
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
        instances: Dict[str, Any] = {}
        for token in tokens:
            instances[token] = self.resolve(token)
        return instances

    def _get_fn_deps(self, fn: Callable) -> Dict[str, InjectionToken]:
        # Get all the parameters of the function
        args: Dict[str, Parameter] = inspect.signature(fn).parameters

        # Get the injection metadata attached to the function
        injects: Dict[str, InjectMetaData] = getattr(fn, INJECT_FN_DEPENDENCY_KEY, {})

        # Map arguments to their corresponding injection tokens
        fn_deps: Dict[str, InjectionToken] = {}
        for arg_name, param in args.items():
            # Check if the parameter has explicit InjectMetaData
            inject_meta: InjectMetaData = injects.get(arg_name)

            if inject_meta:
                # Use the token from InjectMetaData
                fn_deps[arg_name] = inject_meta.token
            else:
                # If no InjectMetaData is provided, fall back to the type annotation
                if param.annotation is not Parameter.empty:
                    fn_deps[arg_name] = param.annotation
                else:
                    raise ValueError(f"Cannot resolve dependency for argument '{arg_name}' in function '{fn.__name__}'")

        return fn_deps


class NullInjector(BaseInjector):
    resolve_status = ResolveStatus.NONE

    def resolve(self, token: InjectionToken = None, scope: InjectionScope = None, optional: bool = False) -> T:
        if optional:
            return None
        else:
            raise Exception(f'Null injector found for {stringify_injection_token(token)}')


NULL_INJECTOR = NullInjector()
