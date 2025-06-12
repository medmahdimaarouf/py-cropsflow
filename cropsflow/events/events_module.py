from cropsflow.common import inject, Init, DynamicModule, ValueProviderMetaData, InjectionToken
from cropsflow.common.decorators import module
from cropsflow.router import Router
from .config import EventsModuleConfig
from .event_emitter import EventEmitter
from .routes import get_events_router

EVENTS_MODULE_CONFIG_INJECTION_TOKEN: InjectionToken = '__events_module_config_injection_token__'


@module(
    providers=[
        EventEmitter,
    ],
    exports=[EventEmitter]
)
class EventsModule(Init):

    @staticmethod
    def config(config: EventsModuleConfig = EventsModuleConfig()) -> DynamicModule:
        """
        Create a configured DynamicModule for EventsModule
        with the given EventsModuleConfig instance.
        """
        return DynamicModule(
            module=EventsModule,
            providers=[
                ValueProviderMetaData(
                    provide=EVENTS_MODULE_CONFIG_INJECTION_TOKEN,
                    use_value=config
                )
            ]
        )

    @inject(arg_name='router', token=Router, optional=True)
    @inject(arg_name='event_emitter', token=EventEmitter, optional=False)
    @inject(arg_name='config', token=EVENTS_MODULE_CONFIG_INJECTION_TOKEN, optional=True)
    async def init(
            self,
            event_emitter: EventEmitter,
            router: Router = None,
            config: EventsModuleConfig = EventsModuleConfig()
    ) -> None:
        """
        Module initialization logic.

        If a router is available, mount the events router.
        """
        if router is not None:
            router.include_router(router=get_events_router(event_emitter=event_emitter))
