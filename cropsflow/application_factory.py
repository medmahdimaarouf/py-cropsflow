import inspect
from typing import Type, Any, Union

from cropsflow.common.abstracts import Init
from cropsflow.common.decorators import InjectionScope, ModuleDef
from cropsflow.core.abstracts import ResolveStatus
from cropsflow.core.engine import TaskTemplateBuilder
from cropsflow.core.exceptions.builder import TaskBuildException
from cropsflow.core.scanner.dependency_scanner import DependenciesScanner
from .application import Application
from .application_options import ApplicationOptions
from .events import EventsModule
from .monitoring import MonitoringModule
from .router import RouterModule


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
                print(inspect.getfile(module.metadata.target))
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
    application: Application = None
    core_modules: list[Union[ModuleDef, Type[Any]]] = []

    def register(self, module: Union[ModuleDef, Type[Any]]) -> 'ApplicationFactory':
        self.core_modules.append(module)
        return self

    async def init(self, t: Type[Any], options: ApplicationOptions = None, overrides: list[Type[any]] = [], args: list[str] = []) -> Application:
        try:
            self.application = Application(args)
            scanner = DependenciesScanner(app=self.application)
            print("Initializing ...")
            print("scanning dependencies ...")
            scanner.scan_modules(t, overrides=overrides)
            scanner.scan_edges()
            scanner.bind_edges()
            print('Modules initializing...')
            await initialize_modules(self.application)
            print('Application initialized successfully')
            print('Building tasks ...')
            build_tasks(self.application)
            return self.application
        except Exception as e:
            if options.debug:
                raise e
            else:
                print(str(e))
                raise e
                return None

    async def start(self, t: Type[Any], options: ApplicationOptions = ApplicationOptions(), args: list[str] = []) -> Application:
        return await self.init(t, options=options, args=args, overrides=[MonitoringModule, RouterModule, EventsModule])
