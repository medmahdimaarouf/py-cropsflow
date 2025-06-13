import sys
from abc import ABC, abstractmethod
from typing import Type, Any, Union

from cropsflow.common import ModuleDef
from cropsflow.core.application import Application
from cropsflow.core.application_options import ApplicationOptions
from cropsflow.core.builder import TaskTemplateBuilder
from cropsflow.core.exceptions.builder import TaskBuildException


class ApplicationPlatform(ABC):

    def __init__(self, **args):
        self.application: Application = Application(args=args)

    async def init(self, module: Type[Any], options: ApplicationOptions = None,
                   overrides: list[Type[any]] = None) -> Application:

        try:
            print('bootstrap application ...')
            await self.application.bootstrap(module=module, overrides=overrides or [])
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
