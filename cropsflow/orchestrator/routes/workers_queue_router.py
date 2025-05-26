from cropsflow.router import Router
from cropsflow.platforms import Application


def get_workers_queue_router(application: Application) -> Router:
    router = Router(prefix='/queue')

    @router.get(path='')
    def handle_route():
        return Router.success({})

    return router
