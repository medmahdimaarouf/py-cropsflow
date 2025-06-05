import asyncio
import threading
import uuid
from enum import Enum
from typing import Optional, Callable

from cropsflow.common.abstracts import TaskContext
from .runner import PlayBookRunner, RunnerFlag
from .worker_monitor import WorkerMonitor


class WorkerStatus(Enum):
    PENDING = 0
    RUNNING = 1
    COMPLETED = 2
    CANCELLED = 3


class Worker(threading.Thread):
    id: str
    monitor: WorkerMonitor = WorkerMonitor()
    status: WorkerStatus = WorkerStatus.PENDING

    def __init__(
            self,
            runner: PlayBookRunner,
            daemon: bool = False,
            on_complete: Optional[Callable[['Worker'], None]] = None
    ):
        self.id = str(uuid.uuid4())
        self.__runner = runner
        self._on_complete_callback = on_complete

        def target():
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            try:
                self._loop.run_until_complete(self.start_async())
            except asyncio.CancelledError:
                print(f"TaskWorker {self.id} was stopped (CancelledError).")
                self.status = WorkerStatus.CANCELLED
            finally:
                self._loop.close()

        super(Worker, self).__init__(target=target, daemon=daemon)

    async def start_async(self):
        context: TaskContext = TaskContext()
        print(f'Running task {self.id} ...')
        self.status = WorkerStatus.RUNNING
        try:
            await self.__runner.run(context=context)
        except asyncio.CancelledError:
            print(f"TaskWorker {self.id} was cancelled during execution.")
            self.status = WorkerStatus.CANCELLED
            raise
        else:
            self.status = WorkerStatus.COMPLETED
            if self.__runner.flag.value == RunnerFlag.ERROR:
                print(f"TaskWorker {self.id} completed with error.")
            else:
                print(f"TaskWorker {self.id} completed.")
            if self._on_complete_callback:
                self._on_complete_callback(self)

    def cancel(self):
        """Cancel the running worker."""
        if self.status != WorkerStatus.RUNNING:
            return  # Not running or already stopped

        print(f"Requesting cancel for TaskWorker {self.id} ...")
        self._cancel_event.set()

        # Thread-safe cancellation: schedule coroutine cancellation in event loop
        def cancel_task():
            for task in asyncio.all_tasks(loop=self._loop):
                task.cancel()

        self._loop.call_soon_threadsafe(cancel_task)
