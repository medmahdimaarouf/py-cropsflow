from cropsflow.router import Router
from cropsflow.platforms import Application
from .workers_queue_router import get_workers_queue_router
from .workers_pool_router import get_workers_pool_router


def get_workers_router(application: Application) -> Router:
    router = Router(prefix='/workers')

    @router.get(path='')
    def handle_route():
        return Router.success({})

    @router.get(path='')
    def handle_route():
        return Router.success({})

    router.include_router(router=get_workers_pool_router(application=application))
    router.include_router(router=get_workers_queue_router(application=application))
    return router
