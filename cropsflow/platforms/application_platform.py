import inspect
import sys
from abc import ABC, abstractmethod
from typing import Type, Any, Union

from cropsflow.common import Init, InjectionScope, ModuleDef
from cropsflow.core.builder import TaskTemplateBuilder
from cropsflow.core.exceptions.builder import TaskBuildException
from cropsflow.core.scanner.dependency_scanner import DependenciesScanner
from .application import Application
from .application_options import ApplicationOptions


class ApplicationPlatform(ABC):

    def __init__(self, **args):
        self.application: Application = Application(args=args)
        self.scanner: DependenciesScanner = DependenciesScanner(app=self.application)

    async def init(self, module: Type[Any], options: ApplicationOptions = None,
                   overrides: list[Type[any]] = []) -> Application:

        try:
            print("Initializing ...")
            print("scanning dependencies ...")
            self.scanner.scan_modules(dep=module, overrides=overrides)
            self.scanner.scan_edges()
            self.scanner.bind_edges()
            print("Loading dependencies ...")
            self.__resolve_dependencies()
            print('Modules initializing...')
            await self.__initialize_modules()
            print('Application initialized successfully')
            print('Building tasks ...')
            self.__build_tasks()
            print('Tasks built successfully')
            return self.application
        except Exception as e:
            if options.debug:
                raise e
            else:
                print(str(e), file=sys.stderr)
                raise e
                return None

    @abstractmethod
    async def start(self, t: Type[Any], options: ApplicationOptions = ApplicationOptions(),
                    args: list[str] = []) -> Application:
        pass

    def register(self, module: Union[ModuleDef, Type[Any]]) -> 'ApplicationFactory':
        self.core_modules.append(module)
        return self

    def __resolve_dependencies(self) -> None:
        for module in self.application.modules.values():
            for dep in module.deps.values():
                dep.injector.resolve(scope=InjectionScope.DEFAULT)
            dep.injector.resolve(scope=InjectionScope.DEFAULT)

    async def __initialize_modules(self) -> None:
        for module in self.application.modules.values():
            instance: Init = module.get().resolve()
            if issubclass(type(instance), Init):
                try:
                    deps = module.injector.resolve_class_method_deps(module.metadata.target, instance.init)
                    await instance.init(**deps)
                    print('initialized module : ', module.get_name())
                except Exception as e:
                    print(inspect.getfile(module.metadata.target))
                    print(f"Error initializing module {module.metadata.target.__name__} : {str(e)}", file=sys.stderr)
                    # print_traceback()
                    raise e

    def __build_tasks(self) -> None:
        has_errors: bool = False

        def error_callback(e: TaskBuildException):
            nonlocal has_errors
            has_errors = True
            if isinstance(e, TaskBuildException):
                print(e.message, file=sys.stderr)
            else:
                print(str(e), file=sys.stderr)

        for token, task in self.application.tasks.items():
            print(f"building task '{task.metadata.target.__name__}' ...")
            TaskTemplateBuilder(task=task).build(error_callback=error_callback)
            if has_errors is not True:
                print(f"build task '{task.metadata.target.__name__}' completed successfully")
            else:
                print(f"build task '{task.metadata.target.__name__}' Failed, file=sys.stderr")
        if has_errors:
            print("Tasks build failed", file=sys.stderr)
            exit(0)
