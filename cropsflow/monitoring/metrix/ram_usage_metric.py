import threading

import psutil

from cropsflow import GaugeMetric


class RAMGaugeMetric(GaugeMetric):
    def __init__(self):
        super().__init__('RAM usage', 'RAM usage per %')
        self.memory = psutil.virtual_memory()

    def collect(self):
        with threading.Lock():
            self.set(self.memory.percent)
