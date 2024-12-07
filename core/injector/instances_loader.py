from core.abstracts import ResolveStatus
from common.decorators import InjectionScope
from core.inspector import Inspector


def load_dependencies(inspector: Inspector):
    for module in inspector.modules.values():
        for dep in module.deps.values():
            dep.resolve_status = ResolveStatus.PENDING
            dep.injector.resolve(scope=InjectionScope.DEFAULT)
