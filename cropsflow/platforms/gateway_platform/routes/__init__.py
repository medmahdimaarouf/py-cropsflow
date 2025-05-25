from .inspector import get_inspector_router
from .workers import get_workers_router
from cropsflow.router import Router
from cropsflow.platforms import Application


def get_api_router(application: Application) -> Router:
    router: Router = application.get(token=Router).resolve()
    router.include_router(router=get_inspector_router(application=application))
    router.include_router(router=get_workers_router(application=application))
    return router
