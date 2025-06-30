from cropsflow.router import Router
from .monitor_router import get_monitor_metrics_router
from ..exceptions import MonitorNotFoundException
from ..monitor import Monitor
from ..monitors_manager import MonitorsManager


def get_monitors_router(monitors_manager: MonitorsManager) -> Router:
    monitor_router: Router = Router(prefix='/monitors')

    @monitor_router.get(path='')
    def get_monitors():
        monitors: list[dict] = []
        for monitor_id in monitors_manager.get_monitors():
            monitor: Monitor = monitors_manager.get_monitor(monitor_id=monitor_id)
            monitors.append({
                "id": monitor.id,
                "name": monitor.name,
                "description": monitor.description
            })
        return Router.success(data=monitors)

    @monitor_router.get(path='/{monitor_id}')
    @monitor_router.handle_exception(MonitorNotFoundException, 404)
    def get_monitor(monitor_id: str):
        monitor = monitors_manager.get_monitor(monitor_id=monitor_id)
        if monitor is not None:
            return Router.success(data={
                "id": monitor.id,
                "name": monitor.name,
                "description": monitor.description
            })
        else:
            raise MonitorNotFoundException()

    monitor_router.include_router(prefix='/{monitor_id}',
                                  router=get_monitor_metrics_router(monitors_manager=monitors_manager))

    return monitor_router
