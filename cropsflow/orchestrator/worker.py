import asyncio

import threading
import uuid
from cropsflow.common.abstracts import TaskContext
from .runner import PlayBookRunner
from .worker_monitor import WorkerMonitor


class Worker(threading.Thread):
    id: str
    monitor: WorkerMonitor = WorkerMonitor()

    def __init__(self, runner: PlayBookRunner, daemon: bool = False):
        self.id = str(uuid.uuid4())
        self.__runner = runner

        def target():
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            try:
                self._loop.run_until_complete(self.start_async())
            except asyncio.CancelledError:
                print(f"TaskWorker {self.id} was stopped.")
            finally:
                self._loop.close()

        super(Worker, self).__init__(target=target, daemon=daemon)

    async def start_async(self):
        context: TaskContext = TaskContext()
        print(f'Running task {self.id} ...')
        await self.__runner.run(context=context)
        print(f"TaskWorker {self.id} completed.")

    def stop(self):
        print(f"Stopping TaskWorker {self.id}...")
        if self._loop:
            # Cancel all running tasks in the loop
            tasks = asyncio.all_tasks(loop=self._loop)
            for task in tasks:
                task.cancel()
            self._loop.call_soon_threadsafe(self._loop.stop)  # Stop the loop
        self._stop_event.set()

    def resume(self):
        print(f"Resuming TaskWorker {self.id}...")
        self._pause_event.set()  # Allow the thread to continue
