from cropsflow.router import Router
from cropsflow.core.application import Application


def get_data_sources_router(application: Application) -> Router:
    router = Router(prefix='/sources')

    @router.get(path='')
    def handle_route():
        return Router.success({})

    return router
