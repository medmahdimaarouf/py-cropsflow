from cropsflow.common.abstracts.event import Event
from cropsflow.router import Router
from ..event_emitter import EventEmitter
from ..exceptions import ChannelNotFoundException
from ..models import EventChannelModel, EventChannelEventModel


def get_channel_events_router(event_emitter: EventEmitter) -> Router:
    channel_event_router: Router = Router(prefix='/events')

    @channel_event_router.get(path='')
    @channel_event_router.handle_exception(ChannelNotFoundException, 404)
    def get_channel_events(channel_id: str):
        channel = event_emitter.get_channel(channel_id=channel_id)

        if channel is None:
            raise ChannelNotFoundException(channel_id)
        else:
            return Router.success(data=[{
                'id': event.id,
                'name': event.name,
                'description': event.description,
                'handlers': len(event.get_handlers())
            } for event in channel.events()])

    @channel_event_router.post(path='')
    @channel_event_router.handle_exception(ChannelNotFoundException, 404)
    def add_channel_event(channel_id: str, model: EventChannelEventModel):
        channel = event_emitter.get_channel(channel_id=channel_id)

        if channel is not None:
            event = Event(event_id=model.get_id(), name=model.name, description=model.description)
            channel.register(event=event)
            return Router.success(data={
                'id': event.id,
                'name': event.name,
                'description': event.description,
                'handlers': len(event.get_handlers())
            })
        else:
            raise ChannelNotFoundException(channel_id)

    return channel_event_router
