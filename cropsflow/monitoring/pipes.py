from typing import Dict, Any

from cropsflow.common import Pipe, pipe, TaskContext, option, DataModel

from .monitor import Monitor
from .metrix import Metric


@pipe(selector='monitor-get-metric-pipe')
@option(key='name', meta_type=str, required=True)
class MonitorGetMetricPipe(Pipe):
    monitor: Monitor

    def __init__(self, monitor: Monitor):
        self.monitor = monitor

    def accumulate(self, context: TaskContext, options: Dict[str, Any] = {}, data: DataModel = None, accessor: str = None) -> None:
        metric_name: str = options.get('name')
        metric: Metric = self.monitor.get_metric(metric_name.strip())
        if metric is not None:
            self.set_data(data=metric.collect())
        else:
            self.set_data(None)
