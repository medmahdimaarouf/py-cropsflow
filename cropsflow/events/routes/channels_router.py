from cropsflow.router import Router
from .channel_events_router import get_channel_events_router
from ..event_emitter import EventEmitter
from ..models import EventChannelModel


def get_channels_router(event_emitter: EventEmitter):
    channels_router: Router = Router(prefix='/channels')

    @channels_router.get('/')
    def handle_route():
        return Router.success(data={
            "activated": True
        })

    @channels_router.get(path='')
    def get_channels():
        return Router.success(data=[{
            "id": channel.id,
            "title": channel.title,
            "createdAt": channel.created_at,
            "description": channel.description
        } for channel in event_emitter.get_channels()])

    @channels_router.post(path='')
    def create_channel(channel: EventChannelModel):
        channel = event_emitter.create_channel(channel_id=channel.get_channel_id(), title=channel.title, description=channel.description)
        return Router.success(data={
            "id": channel.id,
            "title": channel.title,
            "createdAt": channel.created_at,
            "description": channel.description
        })

    @channels_router.get(path='/{channel_id}')
    def get_channel(channel_id: str):
        channel = event_emitter.get_channel(channel_id=channel_id)
        if channel is not None:
            return Router.success(data={
                "id": channel.id,
                "title": channel.title,
                "createdAt": channel.created_at,
                "description": channel.description
            })
        else:
            return Router.error(error=f"channel not found with id '{channel_id}'", status=404)

    @channels_router.delete(path='/{channel_id}')
    def delete_channel(channel_id: str):
        if event_emitter.has_channel(channel_id=channel_id):
            event_emitter.remove_channel(channel_id=channel_id)
            return Router.success(data=True)
        else:
            return Router.error(error=f"channel not found with id '{channel_id}'", status=404)

    channels_router.include_router(router=get_channel_events_router(event_emitter=event_emitter), prefix='/{channel_id}')

    return channels_router
