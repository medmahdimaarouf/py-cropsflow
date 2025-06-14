from typing import Dict, Any

from cropsflow.common import DataAction, action, TaskContext, option, Metric

from cropsflow.monitoring.monitor import Monitor


@action(selector='monitor-get-metric')
@option(key='name', meta_type=str, required=True)
class MonitorGetMetricAction(DataAction[TaskContext, any]):

    def __init__(self, monitor: Monitor):
        super().__init__(data=None)
        self.monitor: Monitor = monitor

    async def run(self, context: TaskContext, options: Dict[str, Any]) -> TaskContext:
        metric_name: str = options.get('name')
        metric: Metric = self.monitor.get_metric(metric_name.strip())
        if metric is not None:
            self.data = metric.collect()
        else:
            self.data = None
        return context
