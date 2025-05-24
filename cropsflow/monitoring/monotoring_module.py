from cropsflow.common import module
from .monitor import Monitor
from .pipes import MonitorGetMetricPipe


@module(
    providers=[
        Monitor
    ],
    declarations=[
        MonitorGetMetricPipe
    ],
    exports=[
        Monitor
    ]
)
class MonitoringModule:
    pass
