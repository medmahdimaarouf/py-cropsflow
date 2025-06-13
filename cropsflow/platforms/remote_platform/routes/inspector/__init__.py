from .get_modules_router import get_modules_router
from cropsflow.router import Router
from cropsflow.core.application import Application


def get_inspector_router(application: Application) -> Router:
    inspector_router = Router(prefix='/inspector')

    @inspector_router.get(path='')
    def handle_route():
        return Router.success({
            "activated": True
        })

    inspector_router.include_router(router=get_modules_router(application=application))

    return inspector_router
