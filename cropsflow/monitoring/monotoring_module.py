"""
This module defines the MonitoringModule which integrates system monitoring metrics into the application.

The module provides a Monitor service that tracks various system metrics such as CPU and RAM usage.
It also exposes HTTP routes to retrieve the registered metrics.
"""

from cropsflow.common import inject, DynamicModule, ValueProviderMetaData, InjectionToken, Init
from cropsflow.common.decorators import module
from cropsflow.router import Router
from .actions import MonitorGetMetricAction
from .config import MonitoringModuleConfig
from .monitors_manager import MonitorsManager
from .monitor import Monitor

MONITORING_MODULE_CONFIG_INJECTION_TOKEN: InjectionToken = '__monitoring_module_config_injection_token__'


@module(
    declarations=[MonitorGetMetricAction],
    providers=[MonitorsManager],
    exports=[MonitorsManager, MonitorGetMetricAction]
)
class MonitoringModule(Init):
    """
    MonitoringModule initializes and configures system monitoring capabilities.

    It registers CPU and RAM gauge metrics to the Monitor service and optionally binds HTTP routes
    to expose metric data.
    """

    @staticmethod
    def config(config: MonitoringModuleConfig = MonitoringModuleConfig()) -> DynamicModule:
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

    @inject(arg_name='router', token=Router, optional=True)
    @inject(arg_name='monitors_manager', token=MonitorsManager, optional=False)
    @inject(arg_name='config', token=MONITORING_MODULE_CONFIG_INJECTION_TOKEN, optional=True)
    async def init(
            self,
            monitors_manager: MonitorsManager,
            router: Router = None,
            config: MonitoringModuleConfig = MonitoringModuleConfig()
    ) -> None:
        """
        Initialize the MonitoringModule by registering metrics and optionally binding routes.

        Args:
            monitors_manager (MonitorsManager): The Monitors manager service to register monitors with.
            router (Router, optional): The router to which monitoring routes will be added.
            config (MonitoringModuleConfig, optional): Configuration object for the module.
        """
        monitor = Monitor()
        # monitor.register_metric(name='CPU Gauge Metric', metric=CPU())
        # monitor.register_metric(name='RAM Gauge Metric', metric=RAMGaugeMetric())
        # monitors_manager.register(monitor=monitor)
        if router is not None:
            monitor_router: Router = Router(prefix='/monitor')

            @monitor_router.get('/')
            def handle_route():
                return Router.success(data=monitor.get_metrix())

            @monitor_router.get(path='metrix')
            def get_metrix():
                return Router.success(data=monitor.get_metrix())

            router.include_router(router=monitor_router)
        else:
            print(f"could not bind routes for monitoring")
