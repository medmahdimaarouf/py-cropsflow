import asyncio
import traceback

from cropsflow import Monitor
from starlette.websockets import WebSocket, WebSocketDisconnect

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

    @monitor_metrics_router.websocket(path="/{metric_id}")
    async def realtime_monitor_metric(websocket: WebSocket, monitor_id: str, metric_id: str):
        monitor: Monitor = monitors_manager.get_monitor(monitor_id=monitor_id)

        async def send_monitor_metric_value(_: str, value: any):
            print("send metric")
            await websocket.send_json({
                "monitor": metric_id,
                "id": metric_id,
                "value": value
            })

        if monitor is not None:
            await websocket.accept()
            try:
                monitor.watch(metric_id=metric_id, callback=send_monitor_metric_value)
                while True:
                    command = await websocket.receive_json()
                    print('received cmd:', command)
            except WebSocketDisconnect:
                monitor.unwatch(metric_id=metric_id, callback=send_monitor_metric_value)
            except Exception as e:
                traceback.print_exception(e)
                monitor.unwatch(metric_id=metric_id, callback=send_monitor_metric_value)
                await websocket.close()
        else:
            await websocket.close()

    return monitor_metrics_router
