from cropsflow.router import Router
from .channel_events_router import get_channel_events_router
from .channels_router import get_channels_router
from ..event_emitter import EventEmitter


def get_events_router(event_emitter: EventEmitter) -> Router:
    events_router: Router = Router(prefix='/events')

    @events_router.get('')
    def handle_route():
        return Router.success(data={"activated": True})

    events_router.include_router(router=get_channels_router(event_emitter=event_emitter))

    return events_router
