import gc
import inspect
import traceback
from abc import abstractmethod, ABC
from asyncio import sleep
from collections import deque
from copy import copy
from enum import Enum
from typing import List, TypeVar, Generic, Callable, Optional, cast

from cropsflow.common import TaskContext, ActionDecoratorMetaData, DecoratorMetaData, InjectionScope, Action, Init, \
    Destroy, Pipe
from cropsflow.core.builder import PlaybookNode, EPlaybookNodeType
from cropsflow.core.utils import BehaviorSubject
from .exceptions import RunnerException

I = TypeVar('I')


class RunnerFlag(Enum):
    READY = 'READY',
    RUNNING = 'RUNNING',
    ERROR = "ERROR",
    STOPPED = 'STOPPED',
    COMPLETED = 'COMPLETED'


class Runner(Generic[I], ABC):

    @property
    def container_metadata(self) -> DecoratorMetaData:
        return self.node.container.metadata

    @property
    def container_class_file(self) -> str:
        return inspect.getfile(self.container_metadata.target)

    def __init__(self, node: PlaybookNode, parent: 'Runner' = None):
        self.node: PlaybookNode = node
        self.parent: 'Runner' = parent
        self.async_runners: List["Runner"] = []
        self.sync_runners: deque["Runner"] = deque()
        self.flag: BehaviorSubject[RunnerFlag] = BehaviorSubject(RunnerFlag.READY)
        self.instance: I = None
        self.context: TaskContext = None
        self.stopped: bool = False

    @abstractmethod
    async def run(self, context: TaskContext) -> None:
        pass

    def stop(self):
        self.flag.next(RunnerFlag.STOPPED)
        for runner in self.sync_runners:
            runner.stop()

    def resume(self):
        self.flag.next(RunnerFlag.RUNNING)
        for runner in self.sync_runners:
            runner.resume()

    async def run_queue(self, context: TaskContext) -> None:
        while len(self.sync_runners) and self.flag.value is RunnerFlag.RUNNING:
            while self.stopped:
                await sleep(500)
            runner = self.sync_runners.popleft()
            if runner.node.is_async:
                self.async_runners.append(runner)
                runner.run(context=copy(context))
            else:
                await runner.run(context=copy(context))

            if runner.flag.value is RunnerFlag.ERROR:
                self.flag.next(RunnerFlag.ERROR)
        gc.collect()

    def init(self, context: TaskContext = None, **args) -> None:
        self.instance = self.node.container.injector.resolve(scope=InjectionScope.TRANSIENT, optional=False)
        self.context = context
        if isinstance(self.instance, Init):
            self.instance.init(args)
        for child_node in self.node.children:
            if child_node.type == EPlaybookNodeType.ACTION:
                self.sync_runners.append(ActionRunner(node=child_node, parent=self))
            if child_node.type == EPlaybookNodeType.PIPE:
                self.sync_runners.append(PipeRunner(node=child_node, parent=self))
        gc.collect()

    def destroy(self, **args) -> None:
        if self.instance is not None and isinstance(self.instance, Destroy) and not self.is_async:
            self.instance.destroy(args)
            del self.instance


class ActionRunner(Runner[Action]):
    async def run(self, context: TaskContext) -> None:
        self.flag.next(RunnerFlag.RUNNING)

        async def next_callback(ctx: TaskContext) -> None:
            await self.run_queue(context=ctx)

        try:
            print(f"running action {self.node.container.get_name()} ...")
            self.init(context=context)
            is_auto_next: bool = cast(ActionDecoratorMetaData, self.node.container.metadata).auto_next

            self.instance.next_callback: Callable[[TaskContext], None] = next_callback if not is_auto_next else None
            next_context = await self.instance.run(context=copy(context), options=self.node.options)
            '''
            @todo some instances doesn't return context , None instead is returned -> rais clear exception and log
            '''
            if is_auto_next:
                await self.run_queue(context=next_context)
            self.flag.next(RunnerFlag.COMPLETED)
            print(f"completed action {self.node.container.get_name()}")
        except Exception as e:
            if not self.node.skippable:
                raise e
            else:
                traceback.print_exception(e)
        finally:
            self.destroy()


class PipeRunner(Runner[Pipe]):

    def __init__(self, node: PlaybookNode, parent: 'Runner' = None):
        super().__init__(node=node, parent=parent)
        self.accumulator_pipe_runner: 'PipeRunner' = self.find_accumulator_pipe_runner(
            accumulator_pipe_id=self.node.accumulator_id)

    def find_accumulator_pipe_runner(self, accumulator_pipe_id: str = None) -> Optional["PipeRunner"]:
        parent: PipeRunner = self.parent
        while parent:
            if isinstance(parent, PipeRunner):
                if accumulator_pipe_id is None or parent.node.options.get("id") == accumulator_pipe_id:
                    return parent
            else:
                parent = parent.parent
        if accumulator_pipe_id is not None:
            raise Exception(f'Could not locate target accumulator pipe with id {self.node.accumulator_id}')
        else:
            return None

    async def run(self, context: TaskContext) -> None:
        self.flag.next(RunnerFlag.RUNNING)
        try:
            print(f"running pipe {self.node.container.get_name()} ...")
            self.init(context=context)
            await self.run_queue(context=context)
            if self.accumulator_pipe_runner:
                self.accumulator_pipe_runner.accumulate(data=self.instance.get_data(),
                                                        accessor=self.node.accumulator_accessor)
            self.flag.next(RunnerFlag.COMPLETED)
            print(f"completed pipe {self.node.container.get_name()}")
        except Exception as e:
            if not self.node.skippable:
                raise e
            else:
                traceback.print_exception(e)
        finally:
            self.destroy()

    def accumulate(self, data: any, accessor: str = None):
        self.instance.accumulate(context=self.context, data=data, accessor=accessor, options=self.node.options)


class PlayBookRunner(Runner[object]):

    async def run(self, context: TaskContext) -> None:
        try:
            self.flag.next(RunnerFlag.RUNNING)
            self.init()
            await self.run_queue(context=context)
            self.flag.next(RunnerFlag.COMPLETED)
            self.destroy()
        except RunnerException as e:
            print(f"Playbook: {self.node.parse_node.template_file_name}:{self.node.parse_node.line}", " error : ",
                  e.__str__())
            # e.print_partial_traceback()
            traceback.print_exception(e)
            self.flag.next(RunnerFlag.ERROR)
        except Exception as e:
            # traceback.print_tb(e.__traceback__)
            traceback.print_exception(e)
            self.flag.next(RunnerFlag.ERROR)
