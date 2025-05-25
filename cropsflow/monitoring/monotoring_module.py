from cropsflow.common import inject, DynamicModule, ValueProviderMetaData, InjectionToken
from cropsflow.common.decorators import module
from cropsflow.router import Router
from .config import MonitoringModuleConfig
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
class MonitoringModule:
    @staticmethod
    def config(config: MonitoringModuleConfig = MonitoringModuleConfig()) -> DynamicModule:
        return DynamicModule(module=MonitoringModule, providers=[ValueProviderMetaData(provide=MONITORING_MODULE_CONFIG_INJECTION_TOKEN, use_value=config)])

    @inject(arg_name='router', token=Router, optional=True)
    @inject(arg_name='event_emitter', token=Monitor, optional=False)
    @inject(arg_name='config', token=MONITORING_MODULE_CONFIG_INJECTION_TOKEN, optional=True)
    def init(self, monitor: Monitor, router: Router = None, config: MonitoringModuleConfig = MonitoringModuleConfig()) -> None:
        if router is not None:
            events_router: Router = Router(prefix='/monitor')

            @events_router.get('/')
            def handle_route():
                return Router.success(data=monitor.get_metrix())

            @events_router.get(path='/metrix')
            def get_metrix():
                return Router.success(data=monitor.get_metrix())

            router.include_router(router=router)
