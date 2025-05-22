from ..decorators import service, InjectionScope


@service(scope=InjectionScope.DEFAULT)
class Logger:
    pass
