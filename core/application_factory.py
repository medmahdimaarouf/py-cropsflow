from typing import Type, Any

from common.abstracts import Init
from .application import Application
from .injector import load_dependencies
from .inspector import Inspector
from .scanner.dependency_scanner import DependencyScanner


def initialize_modules(inspector: Inspector):
    load_dependencies(inspector)
    for module in inspector.modules.values():
        instance: Init = module.get().resolve()
        if issubclass(type(instance), Init):
            instance.init(**module.injector.resolve_all())


def build_tasks(inspector: Inspector) -> bool:
    has_errors: bool = False
    for token, task in inspector.tasks.items():

        def errorCallback(e: Exception):
            nonlocal has_errors
            has_errors = True
            print(str(e))

        print(f"building task '{task.metadata.target.__name__}' ...")
        if task.build(errorCallback) is True:
            print(f"build task '{task.metadata.target.__name__}' completed successfully")
        else:
            print(f"build task '{task.metadata.target.__name__}' Failed")
    return not has_errors


class ApplicationFactory:

    def init(self, t: Type[Any]) -> Application:
        application: Application = Application()
        inspector = Inspector(container=application.container)
        scanner = DependencyScanner(inspector)
        try:
            print("Initializing ...")
            scanner.scan(t)
            print('Modules initializing...')
            initialize_modules(inspector)
            print('Building tasks ...')
            if build_tasks(inspector):
                print('Application initialized successfully')
            else:
                print('Build tasks failed')
        except Exception as e:
            raise e
