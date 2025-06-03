from cropsflow.router import Router
from ..event_emitter import EventEmitter
from ..models import EventChannelModel


def get_channel_events_router(event_emitter: EventEmitter) -> Router:
    channel_event_router: Router = Router(prefix='/events')

    @channel_event_router.get(path='')
    def get_channel_events(channel_id: str):
        return Router.success(data=event_emitter.get_channel(channel_id=channel_id).events())

    return channel_event_router
