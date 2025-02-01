import asyncio
import sys
import traceback
from typing import Type, Any

from cropsflow.common.abstracts import Init
from cropsflow.common.decorators import InjectionScope
from . import print_traceback
from .abstracts import ResolveStatus
from .application import Application
from .engine.task_builder import build_task
from .inspector.inspector import Inspector


def load_dependencies(app: Application):
    for module in app.modules.values():
        for dep in module.deps.values():
            dep.resolve_status = ResolveStatus.PENDING
            dep.injector.resolve(scope=InjectionScope.DEFAULT)


async def initialize_modules(app: Application):
    load_dependencies(app)
    for module in app.modules.values():
        instance: Init = module.get().resolve()
        if issubclass(type(instance), Init):
            try:
                deps = module.injector.resolve_class_method_deps(module.metadata.target, instance.init)
                print(module.get_name())
                await instance.init(**deps)
            except Exception as e:
                print(f"Error initializing module {module.metadata.target.__name__}")
                # print_traceback()
                raise e


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

    async def init(self, t: Type[Any]) -> Application:
        application: Application = Application()
        scanner = Inspector(app=application)
        print("Initializing ...")
        scanner.scan(t)
        print('Modules initializing...')
        await initialize_modules(application)
        print('Building tasks ...')
        build_tasks(application)
        print('Application initialized successfully')

        return application

    def start(self, t: Type[Any], debug: bool = False) -> Application:
        try:
            return self.init(t)
        except Exception as e:
            if debug:
                raise e
            else:
                print(str(e))
                return None
