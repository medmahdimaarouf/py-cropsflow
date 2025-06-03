import inspect

from cropsflow.router import Router
from cropsflow.platforms import Application


def get_modules_router(application: Application) -> Router:
    modules_router = Router(prefix='/modules')

    @modules_router.get(path='')
    def handle_route():
        modules = list()
        for token, module in application.modules.items():
            modules.append({
                "id": module.id,
                "className": module.metadata.target.__name__,
                "classFile": inspect.getfile(module.metadata.target),
                "name": module.get_name(),
                "global": module.is_global,
                "tasks": [{
                    "id": task.id,
                    "name": task.metadata.target.__name__,
                    "className": task.metadata.target.__name__,
                    "classFile": inspect.getfile(task.metadata.target)
                } for task in module.get_tasks()]
            })
        return Router.success(modules)

    return modules_router
