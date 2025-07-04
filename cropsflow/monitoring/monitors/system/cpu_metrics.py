import threading
import time

import psutil

from cropsflow.common.abstracts import GaugeMetric, IndicatorMetric


class CPUPercentUsageMetric(GaugeMetric):
    def __init__(self):
        super().__init__(max_value=100, min_value=0)

    def collect(self):
        print('collecting CPUPercentUsageMetric', time.time())
        return psutil.cpu_percent()


class CPUCountMetric(IndicatorMetric):

    def __init__(self):
        super().__init__(title='CPU Count', description='Collects CPU count', initial=0)

    def collect(self) -> float:
        return psutil.cpu_count()
