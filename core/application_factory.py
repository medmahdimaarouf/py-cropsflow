from typing import Type, Any

from common.abstracts import Init
from common.decorators import TaskDecoratorMetaData
from core.application import Application
from core.injector import load_dependencies
from core.inspector import Inspector
from core.scanner.dependency_scanner import DependencyScanner
from .builder.task_builder import build_task


def initialize_modules(inspector: Inspector):
    load_dependencies(inspector)
    for module in inspector.modules.values():
        instance: Init = module.get().resolve()
        if issubclass(type(instance), Init):
            instance.init(**module.injector.resolve_all())


def build_tasks(inspector: Inspector):
    for token, task in inspector.tasks.items():
        def errorCallback(e: Exception):
            print(str(e))

        print(f"building task '{task.metadata.target.__name__}' ...")
        build_task(task, errorCallback)
        print(f"build task '{task.metadata.target.__name__}' completed successfully")
        return

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
            build_tasks(inspector)
            print('Application initialized successfully')
        except Exception as e:
            raise e
