from cropsflow.core.application import Application
from cropsflow.router import Router
from .inspector import get_inspector_router


def get_api_router(application: Application) -> Router:
    router: Router = application.get(token=Router).resolve()
    router.include_router(router=get_inspector_router(application=application))
    return router
