import threading

import psutil

from cropsflow import GaugeMetric, IndicatorMetric


class RAMPercentUsageMetric(GaugeMetric):
    def __init__(self):
        super().__init__('RAM percent usage', 'RAM usage per %', max_value=100, min_value=0)

    def collect(self) -> float:
        with threading.Lock():
            return self.memory.percent


class RAMUsageMetric(IndicatorMetric):
    def __init__(self):
        super().__init__(name='RAM usage indicator', description='RAM usage indicator')

    def collect(self) -> float:
        with threading.Lock():
            self.amount = psutil.virtual_memory().total
            return psutil.virtual_memory().used
