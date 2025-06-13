from typing import Dict, Any

from cropsflow.common import Pipe, pipe, TaskContext, option, Metric

from ..monitor import Monitor


@pipe(selector='monitor-get-metric-pipe')
@option(key='name', meta_type=str, required=True)
class MonitorGetMetricPipe(Pipe):

    def __init__(self, monitor: Monitor):
        self.monitor: Monitor = monitor

    def accumulate(self, context: TaskContext, options: Dict[str, Any] = {}, data: any = None,
                   accessor: str = None) -> None:
        metric_name: str = options.get('name')
        metric: Metric = self.monitor.get_metric(metric_name.strip())
        if metric is not None:
            self.data = metric.collect()
        else:
            self.data = None
