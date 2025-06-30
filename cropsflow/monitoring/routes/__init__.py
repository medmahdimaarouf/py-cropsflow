from cropsflow.monitoring.monitors_manager import MonitorsManager
from cropsflow.router import Router
from .monitors_router import get_monitors_router


def get_monitoring_router(monitors_manager: MonitorsManager) -> Router:
    monitoring_router = Router(prefix='/monitoring')

    @monitoring_router.get('')
    def handle_route():
        return Router.success(data={"activated": True})

    monitoring_router.include_router(router=get_monitors_router(monitors_manager=monitors_manager))

    return monitoring_router
