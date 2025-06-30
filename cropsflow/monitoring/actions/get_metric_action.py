from typing import Dict, Any

from cropsflow.common import DataAction, action, TaskContext, option, Metric
from ..monitor import Monitor
from ..monitors_manager import MonitorsManager


@action(selector='monitor-get-metric')
@option(key='name', meta_type=str, required=True)
@option(key='monitor', meta_type=str, required=True)
class MonitorGetMetricAction(DataAction[TaskContext, any]):

    def __init__(self, monitors_manager: MonitorsManager):
        super().__init__(data=None)
        self.monitors_manager: MonitorsManager = monitors_manager

    async def run(self, context: TaskContext, options: Dict[str, Any]) -> TaskContext:
        metric_name: str = options.get('name')
        monitor_id: str = options.get('monitor_id')
        monitor: Monitor = self.monitors_manager.get(monitor_id=monitor_id)
        metric: Metric = monitor.get_metric(metric_name.strip())
        if metric is not None:
            self.data = metric.collect()
        else:
            self.data = None
        return context
