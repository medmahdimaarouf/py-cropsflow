from cropsflow.common import inject, Init, DynamicModule, ValueProviderMetaData, InjectionToken
from cropsflow.common.decorators import module
from cropsflow.router import Router
from .config import EventsModuleConfig
from .event_emitter import EventEmitter
from .models import EventChannelModel

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
        return DynamicModule(module=EventsModule, providers=[ValueProviderMetaData(provide=EVENTS_MODULE_CONFIG_INJECTION_TOKEN, use_value=config)])

    @inject(arg_name='router', token=Router, optional=True)
    @inject(arg_name='event_emitter', token=EventEmitter, optional=False)
    @inject(arg_name='config', token=EVENTS_MODULE_CONFIG_INJECTION_TOKEN, optional=True)
    async def init(self, event_emitter: EventEmitter, router: Router = None, config: EventsModuleConfig = EventsModuleConfig()) -> None:
        if router is not None:
            events_router: Router = Router(prefix='/events')

            @events_router.get('/')
            def handle_route():
                return Router.success(data=event_emitter.get_channels())

            @events_router.get(path='/channels')
            def get_channels():
                return Router.success(data=event_emitter.get_channels())

            @events_router.post(path='/channels')
            def create_channel(channel: EventChannelModel):
                return Router.success(data=event_emitter.create_channel(channel_id=channel.id, title=channel.title, description=channel.description))

            @events_router.get(path='/channels/{channel_id}')
            def get_channel(channel_id: str):
                return Router.success(data=event_emitter.get_channel(channel_id=channel_id))

            @events_router.delete(path='/channels/{channel_id}')
            def delete_channel(channel_id: str):
                return Router.success(data=event_emitter.get_channel(channel_id=channel_id).events())

            @events_router.get(path='/channels/{channel_id}/events')
            def get_channel_events(channel_id: str):
                return Router.success(data=event_emitter.get_channel(channel_id=channel_id).events())

            router.include_router(router=events_router)
