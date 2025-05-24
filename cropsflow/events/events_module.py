from cropsflow.common import module, inject, Init
from cropsflow.router import Router
from .event_emitter import EventEmitter
from .models import EventChannelModel


@module(
    declarations=[EventEmitter],
    exports=[EventEmitter]
)
class EventsModule(Init):

    @inject(arg_name='router', token=Router, optional=True)
    def init(self, event_emitter: EventEmitter, router: Router = None) -> None:
        if router is not None:
            events_router: Router = Router(prefix='/events')

            @events_router.get('/')
            def handle_events_get():
                return Router.success(data=event_emitter.get_channels())

            @events_router.get(path='/channels')
            def get_channels():
                return Router.success(data=event_emitter.get_channels())

            @events_router.get(path='/channels/{channel_id}')
            def get_channel(channel_id: str):
                return Router.success(data=event_emitter.get_channel(channel_id=channel_id))

            @events_router.get(path='/channels/{channel_id}/events')
            def get_channel_event(channel_id: str):
                return Router.success(data=event_emitter.get_channel(channel_id=channel_id).events())

            @events_router.delete(path='/channels/{channel_id}/events')
            def handle_events_get_channels(channel_id: str):
                return Router.success(data=event_emitter.get_channel(channel_id=channel_id).events())

            @events_router.post(path='/channels')
            def handle_events_get_channels(channel: EventChannelModel):
                return Router.success(data=event_emitter.create_channel(channel_id=channel.id, title=channel.title, description=channel.description))

            router.include_router(router=router)
