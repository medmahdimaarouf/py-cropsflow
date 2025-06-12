"""
This module defines the MonitoringModule which integrates system monitoring metrics into the application.

The module provides a Monitor service that tracks various system metrics such as CPU and RAM usage.
It also exposes HTTP routes to retrieve the registered metrics.
"""

from cropsflow.common import inject, DynamicModule, ValueProviderMetaData, InjectionToken, Init
from cropsflow.common.decorators import module
from cropsflow.router import Router
from .config import MonitoringModuleConfig
from .metrix import CPUGaugeMetric, RAMGaugeMetric
from .monitor import Monitor
from .pipes import MonitorGetMetricPipe

MONITORING_MODULE_CONFIG_INJECTION_TOKEN: InjectionToken = '__monitoring_module_config_injection_token__'


@module(
    providers=[
        Monitor,
    ],
    declarations=[
        MonitorGetMetricPipe
    ],
    exports=[Monitor]
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
    @inject(arg_name='monitor', token=Monitor, optional=False)
    @inject(arg_name='config', token=MONITORING_MODULE_CONFIG_INJECTION_TOKEN, optional=True)
    async def init(
            self,
            monitor: Monitor,
            router: Router = None,
            config: MonitoringModuleConfig = MonitoringModuleConfig()
    ) -> None:
        """
        Initialize the MonitoringModule by registering metrics and optionally binding routes.

        Args:
            monitor (Monitor): The Monitor service to register metrics with.
            router (Router, optional): The router to which monitoring routes will be added.
            config (MonitoringModuleConfig, optional): Configuration object for the module.
        """
        monitor.register_metric(name='cpu_gauge_metric', metric=CPUGaugeMetric())
        monitor.register_metric(name='ram_gauge_metric', metric=RAMGaugeMetric())

        if router is not None:
            events_router: Router = Router(prefix='/monitor')

            @events_router.get('/')
            def handle_route():
                return Router.success(data=monitor.get_metrix())

            @events_router.get(path='/metrix')
            def get_metrix():
                return Router.success(data=monitor.get_metrix())

            router.include_router(router=events_router)
        else:
            print(f"could not bind routes for monitoring")
