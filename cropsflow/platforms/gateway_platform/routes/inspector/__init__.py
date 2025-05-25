from cropsflow.router import Router
from cropsflow.platforms import Application


def get_inspector_router(application: Application) -> Router:
    router = Router(prefix='/inspector')

    @router.get(path='')
    def handle_route():
        return Router.success({})

    @router.get(path='')
    def handle_route():
        return Router.success({})

    return router
