import asyncio
import gc
import inspect
import traceback
from abc import abstractmethod, ABC
from asyncio import sleep
from collections import deque
from copy import deepcopy
from enum import Enum
from typing import List, TypeVar, Generic, Callable, Optional, cast

from cropsflow.common.abstracts import TaskContext, Action, Init, Destroy, Pipe, DataAction
from cropsflow.common.constants import PLAYBOOK_TRANSFORMER_PIPE_ID_OPTION_KEY, PLAYBOOK_RUNNER_OVERRIDE_CONTEXT_ID_KEY
from cropsflow.common.decorators import ActionDecoratorMetaData, DecoratorMetaData, InjectionScope
from cropsflow.core.builder import PlaybookNode, EPlaybookNodeType
from cropsflow.core.utils import BehaviorSubject
from .exceptions import RunnerException

I = TypeVar('I')


class RunnerStatus(Enum):
    READY = 'READY',
    RUNNING = 'RUNNING',
    ERROR = "ERROR",
    STOPPED = 'STOPPED',
    TERMINATED = 'TERMINATED'


class Runner(Generic[I], ABC):

    @property
    def container_metadata(self) -> DecoratorMetaData:
        return self.node.container.metadata

    @property
    def container_metadata(self) -> DecoratorMetaData:
        return self.node.container.metadata

    @property
    def id(self) -> str:
        return self.node.options.get('id', None) or self.node.id

    def __init__(self, node: PlaybookNode, parent: 'Runner' = None):
        self.node: PlaybookNode = node
        self.parent: 'Runner' = parent
        self.async_runners: List["Runner"] = []
        self.sync_runners: deque["Runner"] = deque()
        self.status: BehaviorSubject[RunnerStatus] = BehaviorSubject(RunnerStatus.READY)
        self.instance: I = None
        self.context: TaskContext = None

    @abstractmethod
    async def run(self, context: TaskContext) -> None:
        pass

    def stop(self):
        self.status.next(RunnerStatus.STOPPED)
        for runner in self.sync_runners:
            runner.stop()

    def resume(self):
        self.status.next(RunnerStatus.RUNNING)
        for runner in self.sync_runners:
            runner.resume()

    async def run_queue(self, context: TaskContext) -> None:
        for child_node in self.node.children:
            if child_node.type == EPlaybookNodeType.ACTION:
                self.sync_runners.append(ActionRunner(node=child_node, parent=self))
            if child_node.type == EPlaybookNodeType.PIPE:
                self.sync_runners.append(PipeRunner(node=child_node, parent=self))
        while len(self.sync_runners):
            runner = self.sync_runners.popleft()
            if runner.node.is_async:
                self.async_runners.append(runner)
                runner.run(context=deepcopy(context))
            else:
                await runner.run(context=deepcopy(context))
        gc.collect()

    def init(self, context: TaskContext = None, **args) -> None:
        self.instance = self.node.container.injector.resolve(scope=InjectionScope.TRANSIENT, optional=False)
        if isinstance(self.instance, Init):
            self.instance.init(args)

        if self.node.options.get(PLAYBOOK_RUNNER_OVERRIDE_CONTEXT_ID_KEY, None) is not None:
            self.context = deepcopy(
                self.find_first_runner(runner_id=self.node.options.get(PLAYBOOK_RUNNER_OVERRIDE_CONTEXT_ID_KEY),
                                       optional=False).context)
        elif self.node.options.get('no-context', None) is True:
            self.context = None
        elif self.node.options.get('new-context', None) is True:
            self.context = TaskContext()
        else:
            self.context = context

    def find_first_pipe_runner(self, transformer_pipe_id: str = None, optional: bool = False) -> Optional['PipeRunner']:
        parent: PipeRunner = self.parent
        while parent:
            if isinstance(parent, PipeRunner):
                if transformer_pipe_id is None or parent.id == transformer_pipe_id:
                    return parent
            else:
                parent = parent.parent
        if transformer_pipe_id is not None and not optional:
            raise Exception(f'Could not locate target accumulator pipe with id {self.node.transformer_pipe_id}')
        else:
            return None

    def find_first_runner(self, runner_id: str = None, optional: bool = False) -> Optional['Runner']:
        parent: PipeRunner = self.parent
        while parent:
            if runner_id is None or parent.id == runner_id:
                return parent
            else:
                parent = parent.parent
        if runner_id is not None and not optional:
            raise Exception(f'Could not locate target runner node with id {self.node.transformer_pipe_id}')
        else:
            return None

    def transform(self):
        if isinstance(self.instance, Pipe) or isinstance(self.instance, DataAction):
            transformer_pipe_runner: "PipeRunner" = self.find_first_pipe_runner(
                transformer_pipe_id=self.node.options.get(PLAYBOOK_TRANSFORMER_PIPE_ID_OPTION_KEY))
            if transformer_pipe_runner:
                transformer_pipe_runner.instance.transform(data=self.instance.get_data(), options=self.node.options)

    def destroy(self, **args) -> None:
        if self.instance is not None and isinstance(self.instance, Destroy) and not self.is_async:
            self.instance.destroy(args)
            del self.instance

    async def __check_running_state(self) -> bool:
        if self.status is RunnerStatus.STOPPED:
            while self.status is RunnerStatus.STOPPED:
                await asyncio.sleep(500)

        if self.status.value is RunnerStatus.RUNNING or self.status.value is RunnerStatus.READY:
            return True
        else:
            return False


class ActionRunner(Runner[Action]):
    async def run(self, context: TaskContext) -> None:
        async def next_callback(ctx: TaskContext) -> None:
            await self.run_queue(context=ctx)

        try:
            print(f"running action {self.node.container.get_name()} ...")
            self.init(context=context)
            is_auto_next: bool = cast(ActionDecoratorMetaData, self.node.container.metadata).auto_next

            self.instance.next_callback: Callable[[TaskContext], None] = next_callback if not is_auto_next else None
            next_context = await self.instance.run(context=self.context, options=self.node.options)
            if is_auto_next:
                if next_context is None:
                    raise Exception(f"None context detected for a non auto-next action: {self.node.parse_node.line}")
                await self.run_queue(context=next_context)
            self.transform()
            print(f"completed action {self.node.container.get_name()}")
        except Exception as e:
            if not self.node.skippable:
                raise e
            else:
                traceback.print_exception(e)
        finally:
            self.destroy()


class PipeRunner(Runner[Pipe]):

    async def run(self, context: TaskContext) -> None:
        try:
            print(f"running pipe {self.node.container.get_name()} ...")
            self.init(context=context)
            await self.run_queue(context=self.context)
            self.transform()
            print(f"completed pipe {self.node.container.get_name()}")
        except Exception as e:
            if not self.node.skippable:
                raise e
            else:
                traceback.print_exception(e)
        finally:
            self.destroy()


class PlayBookRunner(Runner[object]):

    async def run(self, context: TaskContext) -> None:
        try:
            self.init()
            await self.run_queue(context=context)
            self.destroy()
        except RunnerException as e:
            print(f"Playbook: {self.node.parse_node.template_file_name}:{self.node.parse_node.line}", " error : ",
                  e.__str__())
            # e.print_partial_traceback()
            traceback.print_exception(e)
        except Exception as e:
            # traceback.print_tb(e.__traceback__)
            traceback.print_exception(e)
