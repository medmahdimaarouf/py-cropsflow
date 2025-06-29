from cropsflow.common.decorators import deps, module, exports
from .scheduers_manager import SchedulersManager


@deps(SchedulersManager)
@exports(SchedulersManager)
@module()
class SchedulerModule:
    pass
