from typing import Dict

from cropsflow.common.abstracts import Metric
from cropsflow.common import service, InjectionScope


@service(scope=InjectionScope.DEFAULT)
class Monitor:

    def __init__(self):
        self.name: str = ''
        self.metrix: Dict[str, Metric] = {}

    def register_metric(self, name: str, metric: Metric) -> Metric:
        if name.strip() not in self.metrix:
            self.metrix.setdefault(name.strip(), metric)
        else:
            raise Exception(f"Enable to add metric: metric name '{name.strip()}' is already exists")

    def get_metric(self, name: str) -> Metric | None:
        return self.metrix.get(name.strip(), None)

    def has_metric(self, name: str) -> bool:
        return name.strip() in self.metrix

    def get_metrix(self) -> list[str]:
        return list(self.metrix.keys())
