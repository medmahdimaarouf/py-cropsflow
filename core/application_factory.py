from typing import Type, Any

from common.abstracts import Init
from common.decorators import InjectionScope
from .abstracts import ResolveStatus
from .application import Application
from .engine.task_builder import build_task
from core.inspector.inspector import Inspector


def load_dependencies(app: Application):
    for module in app.modules.values():
        for dep in module.deps.values():
            dep.resolve_status = ResolveStatus.PENDING
            dep.injector.resolve(scope=InjectionScope.DEFAULT)


def initialize_modules(app: Application):
    load_dependencies(app)
    for module in app.modules.values():
        instance: Init = module.get().resolve()
        if issubclass(type(instance), Init):
            instance.init(**module.injector.resolve_all())


def build_tasks(app: Application):
    has_errors: bool = False
    for token, task in app.tasks.items():

        def errorCallback(e: Exception):
            nonlocal has_errors
            has_errors = True
            print(str(e))

        print(f"building task '{task.metadata.target.__name__}' ...")

        build_task(task=task, error_callback=errorCallback)

        if has_errors is True:
            print(f"build task '{task.metadata.target.__name__}' completed successfully")
        else:
            print(f"build task '{task.metadata.target.__name__}' Failed")
    if has_errors:
        raise Exception("Tasks build failed")


class ApplicationFactory:

    def init(self, t: Type[Any]) -> Application:
        application: Application = Application()
        scanner = Inspector(app=application)
        print("Initializing ...")
        scanner.scan(t)
        print('Modules initializing...')
        initialize_modules(application)
        print('Building tasks ...')
        build_tasks(application)
        print('Application initialized successfully')

        return application

    def start(self, t: Type[Any]) -> Application:
        try:
            return self.init(t)
        except Exception as e:
            print(str(e))
            return None
