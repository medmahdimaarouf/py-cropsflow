"""
This module defines the MonitoringModule which integrates system monitoring metrics into the application.

The module provides a Monitor service that tracks various system metrics such as CPU and RAM usage.
It also exposes HTTP routes to retrieve the registered metrics.
"""
import traceback

from cropsflow.common import inject, DynamicModule, ValueProviderMetaData, InjectionToken, Init
from cropsflow.common.decorators import module
from cropsflow.router import Router
from .actions import MonitorGetMetricAction
from .config import MonitoringModuleConfig
from .monitors import CPUPercentUsageMetric, RAMPercentUsageMetric
from .monitors_manager import MonitorsManager
from .monitor import Monitor
from .routes import get_monitoring_router

MONITORING_MODULE_CONFIG_INJECTION_TOKEN: InjectionToken = '__monitoring_module_config_injection_token__'
DEFAULT_MONITORING_MODULE_CONFIG: MonitoringModuleConfig = MonitoringModuleConfig()


@module(
    declarations=[MonitorGetMetricAction],
    providers=[MonitorsManager,
               ValueProviderMetaData(provide=MONITORING_MODULE_CONFIG_INJECTION_TOKEN,
                                     use_value=DEFAULT_MONITORING_MODULE_CONFIG)],
    exports=[MonitorsManager, MonitorGetMetricAction]
)
class MonitoringModule(Init):
    """
    MonitoringModule initializes and configures system monitoring capabilities.

    It registers CPU and RAM gauge metrics to the Monitor service and optionally binds HTTP routes
    to expose metric data.
    """

    @inject(arg_name='router', token=Router, optional=True)
    @inject(arg_name='monitors_manager', token=MonitorsManager, optional=False)
    @inject(arg_name='config', token=MONITORING_MODULE_CONFIG_INJECTION_TOKEN, optional=True)
    def __init__(self,
                 monitors_manager: MonitorsManager,
                 router: Router = None,
                 config: MonitoringModuleConfig = DEFAULT_MONITORING_MODULE_CONFIG):
        self.monitors_manager: MonitorsManager = monitors_manager
        self.router: Router = router
        self.config: MonitoringModuleConfig = config

    @staticmethod
    def config(config: MonitoringModuleConfig) -> DynamicModule:
        """
        Create a dynamic module configuration for MonitoringModule.

        Args:
            config (MonitoringModuleConfig): Optional configuration for the monitoring module.

        Returns:
            DynamicModule: The dynamic module with configuration providers.
        """
        return DynamicModule(
            module=MonitoringModule,
            providers=[ValueProviderMetaData(provide=MONITORING_MODULE_CONFIG_INJECTION_TOKEN, use_value=config)]
        )

    async def init(self) -> None:
        """
        Initialize the MonitoringModule by registering metrics and optionally binding routes.
        """
        self.register_default_monitors()
        self.bind_routes()
        self.restart_monitors()

    def bind_routes(self):
        if self.router is not None:
            self.router.include_router(router=get_monitoring_router(monitors_manager=self.monitors_manager))

    def register_default_monitors(self) -> None:
        system_monitor: Monitor = Monitor()
        system_monitor.register_metric(name='CPU Gauge Metric', metric=CPUPercentUsageMetric())
        system_monitor.register_metric(name='RAM Gauge Metric', metric=RAMPercentUsageMetric())
        self.monitors_manager.register(name='System Performance Monitor', monitor=system_monitor,
                                       description='Monitor System Performance with metrics')

    def restart_monitors(self) -> None:
        for monitor_id in self.monitors_manager.get_monitors():
            monitor: Monitor = self.monitors_manager.get_monitor(monitor_id=monitor_id)
            if isinstance(monitor, Init):
                try:
                    print(f"[Start] initializing monitor '{monitor.name}'...")
                    monitor.init()
                except Exception as e:
                    print(f"[Error] Enable to init monitor {monitor.name}")
                    traceback.print_exception(e)

            monitor.start()
            print(f"[Start] started monitor '{monitor.name}'")
        if self.router is not None:
            self.router.include_router(router=get_monitoring_router(monitors_manager=self.monitors_manager))
