from typing import Type, Any

from common.abstracts import Init
from common.decorators import InjectionScope
from .abstracts import ResolveStatus
from .application import Application
from .engine.task_builder import build_task
from .inspector import Inspector
from .scanner.dependency_scanner import DependencyScanner


def load_dependencies(inspector: Inspector):
    for module in inspector.modules.values():
        for dep in module.deps.values():
            dep.resolve_status = ResolveStatus.PENDING
            dep.injector.resolve(scope=InjectionScope.DEFAULT)


def initialize_modules(app: Application):
    load_dependencies(app)
    for module in app.modules.values():
        instance: Init = module.get().resolve()
        if issubclass(type(instance), Init):
            instance.init(**module.injector.resolve_all())


def build_tasks(app: Application) -> bool:
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
    return not has_errors


class ApplicationFactory:

    def init(self, t: Type[Any]) -> Application:
        application: Application = Application()
        scanner = DependencyScanner(app=application)
        try:
            print("Initializing ...")
            scanner.scan(t)
            print('Modules initializing...')
            initialize_modules(application)
            print('Building tasks ...')
            if build_tasks(application):
                print('Application initialized successfully')
            else:
                print('Build tasks failed')
        except Exception as e:
            raise e
        return application
