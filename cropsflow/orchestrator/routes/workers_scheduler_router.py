from cropsflow.router import Router
from cropsflow.platforms import Application


def get_workers_scheduler_router(application: Application) -> Router:
    router = Router(prefix='/scheduler')

    @router.get(path='')
    def handle_route():
        return Router.success({})

    return router
