from typing import Type, Dict, Union

from .runner import PlayBookRunner
from .task_builder import TaskTemplateBuilder
from .task_worker import TaskWorker
from .workers_queue import WorkersQueue
from .workers_schedular import WorkersSchedular
from ..injector import Container


class Engine:
    container: Container
    workers: Dict[str, TaskWorker]
    queue: WorkersQueue = WorkersQueue()
    schedular: WorkersSchedular = WorkersSchedular()

    def __init__(self, container: Container):
        self.container = container
        self.workers = {}

    def create_worker(self, meta_type: Type) -> TaskWorker:
        task: Container = self.container.get_task(meta_type)
        if task is None:
            raise Exception(f'Unknown task class {meta_type.__name__}')
        template = TaskTemplateBuilder(task=task).build()
        worker = TaskWorker(runner=PlayBookRunner(node=template.playbook))
        self.workers[worker.id] = worker
        return worker

    def get_worker(self, worker_id: str) -> Union[TaskWorker, None]:
        return self.workers.get(worker_id, None)

    def start_worker(self, worker_id: str) -> None:
        worker: TaskWorker = self.workers.get(worker_id, None);
        if worker is not None:
            worker.run()

    def terminate_worker(self, worker_id: str) -> None:
        worker: TaskWorker = self.workers.get(worker_id, None);
        if worker is not None:
            worker.stop()
        self.workers.pop(worker_id, None)
