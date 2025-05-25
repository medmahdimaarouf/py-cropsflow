from cropsflow.router import Router
from cropsflow.platforms import Application


def get_workers_pool_router(application: Application) -> Router:
    router = Router(prefix='/pool')

    @router.get(path='')
    def handle_route():
        return Router.success({})

    return router
