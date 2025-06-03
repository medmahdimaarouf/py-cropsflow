import threading

import psutil

from cropsflow.common import GaugeMetric


class CPUGaugeMetric(GaugeMetric):
    def __init__(self):
        super().__init__(title='CPU Usage', description='Collects CPU usage per %')

    def collect(self):
        with threading.Lock():
            self.set(psutil.cpu_percent())
