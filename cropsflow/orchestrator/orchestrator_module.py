from cropsflow.common import Init
from cropsflow.common.decorators import module, inject
from cropsflow.core.application import Application
from cropsflow.router import Router
from .orchestrator import Orchestrator
from .routes import *


@module(
    providers=[Orchestrator],
    exports=[Orchestrator]
)
class OrchestratorModule(Init):
    @inject(arg_name='application', token=Application, optional=False)
    @inject(arg_name='router', token=Router, optional=True)
    async def init(self, application: Application, router: Router) -> None:
        if router is not None:
            orchestrator_router = Router(prefix='/orchestrator')
            orchestrator_router.include_router(router=get_workers_scheduler_router(application=application))
            orchestrator_router.include_router(router=get_workers_queue_router(application=Application))
            orchestrator_router.include_router(router=get_workers_pool_router(application=application))
            router.include_router(router=orchestrator_router)
