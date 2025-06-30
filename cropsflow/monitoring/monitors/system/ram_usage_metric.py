import threading

import psutil

from cropsflow import GaugeMetric, IndicatorMetric


class RAMPercentUsageMetric(GaugeMetric):
    def __init__(self):
        super().__init__(max_value=100, min_value=0)

    def collect(self) -> float:
        with threading.Lock():
            return psutil.virtual_memory().percent


class RAMUsageMetric(IndicatorMetric):
    def __init__(self):
        super().__init__(initial=0)

    def collect(self) -> float:
        with threading.Lock():
            self.amount = psutil.virtual_memory().total
            return psutil.virtual_memory().used
