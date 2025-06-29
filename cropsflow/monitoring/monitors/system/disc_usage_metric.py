import threading

import psutil

from cropsflow.common import GaugeMetric, IndicatorMetric


class DiscPercentUsageMetric(GaugeMetric):
    def __init__(self):
        super().__init__(title='CPU Usage', description='Collects CPU usage per %', max_value=100, min_value=0)

    def collect(self):
        with threading.Lock():
            self.set(psutil.disk_usage().percent)


class DiscTotalMetric(IndicatorMetric[float]):
    def __init__(self):
        super().__init__(title='CPU Usage', description='Collects CPU usage per %', initial=0)

    def collect(self) -> float:
        with threading.Lock():
            return psutil.disk_usage().total


class DiscUsedMetric(IndicatorMetric[float]):
    def __init__(self):
        super().__init__(title='CPU Usage', description='Collects CPU usage per %')

    def collect(self) -> float:
        with threading.Lock():
            self.amount = psutil.disk_usage().total
            return psutil.disk_usage().used
