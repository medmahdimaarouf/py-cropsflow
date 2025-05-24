from cropsflow.common import module, Init, DynamicModule
from .router import Router
from .. import inject, Injector


@module(
    providers=[Router],
    exports=[Router]
)
class RouterModule:
    pass


'''
    @inject(arg_name='router', token=Router, optional=True)
    def init(self, injector: Injector, router: Router) -> None:
        pass
'''
