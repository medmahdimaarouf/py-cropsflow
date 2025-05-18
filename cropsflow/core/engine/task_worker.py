import asyncio
import threading
import uuid
from cropsflow.common.abstracts import TaskContext
from cropsflow.core.builder.task_builder import TaskPlaybook


class TaskWorker(threading.Thread):
    id: str
    playbook: TaskPlaybook
    _stop_event = threading.Event()
    _pause_event = threading.Event()
    _loop = None

    def __init__(self, playbook: TaskPlaybook, daemon: bool = False):
        self.id = str(uuid.uuid4())
        self.playbook = playbook
        self._pause_event.set()  # Ensure it starts unpaused

        def target():
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            try:
                self._loop.run_until_complete(self.start_async())
            except asyncio.CancelledError:
                print(f"TaskWorker {self.id} was stopped.")
            finally:
                self._loop.close()

        super(TaskWorker, self).__init__(target=target, daemon=daemon)

    async def start_async(self):
        context: TaskContext = TaskContext()
        for playbook_node in self.playbook:
            await playbook_node.run(context=context)
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

    def pause(self):
        print(f"Pausing TaskWorker {self.id}...")
        self._pause_event.clear()  # Will cause _pause_if_needed to block

    def resume(self):
        print(f"Resuming TaskWorker {self.id}...")
        self._pause_event.set()  # Allow the thread to continue
