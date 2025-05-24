from typing import Type, Any

from cropsflow.common.abstracts import Init
from cropsflow.common.decorators import InjectionScope
from cropsflow.core.abstracts import ResolveStatus
from .application import Application
from .application_options import ApplicationOptions
from cropsflow.core.scanner.dependency_scanner import DependenciesScanner
from cropsflow.core.exceptions.builder import TaskBuildException
from cropsflow.core.engine import TaskTemplateBuilder


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
                print('initializing module : ', module.get_name())
                await instance.init(**deps)
            except Exception as e:
                print(f"Error initializing module {module.metadata.target.__name__}")
                # print_traceback()
                raise e


def build_tasks(app: Application):
    has_errors: bool = False

    def errorCallback(e: TaskBuildException):
        nonlocal has_errors
        has_errors = True
        if isinstance(e, TaskBuildException):
            print(e.message)
        else:
            print(str(e))

    for token, task in app.tasks.items():
        print(f"building task '{task.metadata.target.__name__}' ...")
        TaskTemplateBuilder(task=task).build(error_callback=errorCallback)
        if has_errors is not True:
            print(f"build task '{task.metadata.target.__name__}' completed successfully")
        else:
            print(f"build task '{task.metadata.target.__name__}' Failed")
    if has_errors:
        print("Tasks build failed")
        exit(0)


class ApplicationFactory:

    async def init(self, t: Type[Any], options: ApplicationOptions = None, args: list[str] = []) -> Application:
        try:
            application: Application = Application(args)
            scanner = DependenciesScanner(app=application)
            print("Initializing ...")
            print("scanning dependencies ...")
            scanner.scan_dependencies(t)
            print('Modules initializing...')
            await initialize_modules(application)
            print('Application initialized successfully')
            print('Building tasks ...')
            build_tasks(application)
            return application
        except Exception as e:
            if options.debug:
                raise e
            else:
                print(str(e))
                raise e
                return None

    async def start(self, t: Type[Any], options: ApplicationOptions = ApplicationOptions(), args: list[str] = []) -> Application:
        return await self.init(t, options=options, args=args)
