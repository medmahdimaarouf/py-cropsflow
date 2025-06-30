from cropsflow.monitoring.monitor import Monitor
from .cpu_metrics import CPUPercentUsageMetric


class SystemMonitor(Monitor):
    def __init__(self):
        super().__init__()
        self.register_metric(name='CPU Percent Usage', description='Collects CPU usage per %',
                             metric=CPUPercentUsageMetric())

    def __register_metrics(self):
        pass
