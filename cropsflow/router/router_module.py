from cropsflow.common.decorators import module
from .router import Router


@module(
    providers=[Router],
    exports=[Router],
)
class RouterModule:
    pass


'''
    @inject(arg_name='router', token=Router, optional=True)
    def init(self, injector: Injector, router: Router) -> None:
        pass
'''
