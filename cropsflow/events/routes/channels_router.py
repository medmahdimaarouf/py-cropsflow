from cropsflow.router import Router
from .channel_events_router import get_channel_events_router
from ..event_emitter import EventEmitter
from ..exceptions import DuplicatedChannelException, ChannelNotFoundException
from ..models import EventChannelModel


def get_channels_router(event_emitter: EventEmitter):
    channels_router: Router = Router(prefix='/channels')

    @channels_router.get(path='')
    def get_channels():
        return Router.success(data=[{
            "id": channel.id,
            "name": channel.name,
            "createdAt": channel.created_at,
            "description": channel.description
        } for channel in event_emitter.get_channels()])

    @channels_router.post(path='')
    @channels_router.handle_exception(DuplicatedChannelException, 401)
    def create_channel(channel: EventChannelModel):
        channel = event_emitter.create_channel(name=channel.name, description=channel.description)
        return Router.success(data={
            "id": channel.id,
            "name": channel.name,
            "createdAt": channel.created_at,
            "description": channel.description
        })

    @channels_router.get(path='/{channel_id}')
    @channels_router.handle_exception(ChannelNotFoundException, 404)
    def get_channel(channel_id: str):
        channel = event_emitter.get_channel(channel_id=channel_id)
        if channel is not None:
            return Router.success(data={
                "id": channel.id,
                "name": channel.name,
                "createdAt": channel.created_at,
                "description": channel.description
            })
        else:
            raise ChannelNotFoundException(channel_id)

    @channels_router.delete(path='/{channel_id}')
    @channels_router.handle_exception(ChannelNotFoundException, 404)
    def delete_channel(channel_id: str):
        if event_emitter.has_channel(channel_id=channel_id):
            event_emitter.remove_channel(channel_id=channel_id)
            return Router.success(data=True)
        else:
            raise ChannelNotFoundException(channel_id)

    channels_router.include_router(prefix='/{channel_id}',
                                   router=get_channel_events_router(event_emitter=event_emitter))

    return channels_router
