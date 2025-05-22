from ..decorators import service, InjectionScope


@service(scope=InjectionScope.DEFAULT)
class Monitor:
    pass
