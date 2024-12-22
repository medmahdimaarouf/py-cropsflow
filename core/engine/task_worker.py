import asyncio
import threading
import uuid

from common.abstracts import TaskContext
from .task_builder import TaskPlaybook


class TaskWorker:
    id: str
    playbook: TaskPlaybook

    def __init__(self, playbook: TaskPlaybook):
        self.id = str(uuid.uuid4())
        self.playbook = playbook
        self._stop_flag = threading.Event()
        self._pause_event = threading.Event()
        self._pause_event.set()  # Ensure it starts unpaused

        def thread_logic():
            loop = asyncio.new_event_loop()  # Create a new event loop for the worker
            asyncio.set_event_loop(loop)  # Set it as the current event loop
            loop.run_until_complete(self.start_async())  # Run the async method

        self._thread = threading.Thread(target=thread_logic, daemon=True)

    def start(self):
        print(f"Starting TaskWorker {self.id}...")
        self._thread.start()

    async def start_async(self):
        context: TaskContext = TaskContext()
        for playbook_node in self.playbook:
            await playbook_node.run(context=context)
        print(f"TaskWorker {self.id} completed.")

    def stop(self):
        print(f"Stopping TaskWorker {self.id}...")
        self._stop_flag.set()
        self._pause_event.set()  # Ensure it doesn't hang in pause

    def pause(self):
        print(f"Pausing TaskWorker {self.id}...")
        self._pause_event.set()
        self._pause_event.wait()

    def resume(self):
        print(f"Resuming TaskWorker {self.id}...")
        self._pause_event.clear()
