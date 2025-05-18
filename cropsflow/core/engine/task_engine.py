from typing import Type, Dict, Union

from .task_worker import TaskWorker
from ..application import Application
from ..builder.task_builder import build_task


class Engine:
    application: Application
    workers: Dict[str, TaskWorker]

    def __init__(self, application: Application):
        self.application = application
        self.workers = {}

    def create_worker(self, meta_type: Type) -> TaskWorker:
        task = self.application.task(meta_type)
        template = build_task(task)
        worker = TaskWorker(playbook=template.playbook)
        self.workers[worker.id] = worker
        return worker

    def get_worker(self, worker_id) -> Union[TaskWorker, None]:
        return self.workers.get(worker_id, None)

    def stop_worker(self, worker_id: str) -> None:
        worker: TaskWorker = self.workers.get(worker_id, None);
        if worker is not None:
            worker.stop()

    def start_worker(self, worker_id: str) -> None:
        worker: TaskWorker = self.workers.get(worker_id, None);
        if worker is not None:
            worker.run()

    def pause_worker(self, worker_id: str) -> None:
        worker: TaskWorker = self.workers.get(worker_id, None);
        if worker is not None:
            worker.pause()

    def terminate_worker(self, worker_id: str) -> None:
        worker: TaskWorker = self.workers.get(worker_id, None);
        if worker is not None:
            worker.stop()
        self.workers.pop(worker_id, None)
