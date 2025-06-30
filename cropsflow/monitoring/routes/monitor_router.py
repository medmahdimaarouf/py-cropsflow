from cropsflow.common.abstracts import Metric
from cropsflow.router import Router
from ..exceptions import MonitorNotFoundException
from ..monitors_manager import MonitorsManager


def get_monitor_metrics_router(monitors_manager: MonitorsManager) -> Router:
    monitor_metrics_router: Router = Router(prefix='/metrics')

    @monitor_metrics_router.get(path='')
    @monitor_metrics_router.handle_exception(MonitorNotFoundException, 404)
    def get_monitor_metrics(monitor_id: str):
        monitor = monitors_manager.get_monitor(monitor_id=monitor_id)
        metrics: list[dict] = []
        for metric_id in monitor.get_metrics():
            metric: Metric = monitor.get_metric(metric_id=metric_id)
            metrics.append({
                'id': metric.id,
                'name': metric.name,
                'description': metric.description,
                'value': len(metric.value)
            })
        if monitor is None:
            raise MonitorNotFoundException()
        else:
            return Router.success(data=[])

    return monitor_metrics_router
