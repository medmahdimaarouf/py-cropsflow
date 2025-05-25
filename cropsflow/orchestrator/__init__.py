from typing import Type, Union

from cropsflow.common.decorators import service
from cropsflow.core.builder import *
from .runner import *
from .worker import *
from .worker_factory import *
from .workers_pool import *
from .workers_queue import *
from .workers_scheduler import *


@service(scope=InjectionScope.DEFAULT)
class Orchestrator:
    container: Container
    workers: Dict[str, Worker]
    queue: WorkersQueue = WorkersQueue()
    scheduler: WorkersScheduler = WorkersScheduler()

    def __init__(self, container: Container):
        self.container = container
        self.workers = {}

    def create_worker(self, meta_type: Type) -> Worker:
        task: Container = self.container.get_task(meta_type)
        if task is None:
            raise Exception(f'Unknown task class {meta_type.__name__}')
        template = TaskTemplateBuilder(task=task).build()
        worker = Worker(runner=PlayBookRunner(node=template.playbook))
        self.workers[worker.id] = worker
        return worker

    def get_worker(self, worker_id: str) -> Union[Worker, None]:
        return self.workers.get(worker_id, None)

    def start_worker(self, worker_id: str) -> None:
        worker: Worker = self.workers.get(worker_id, None);
        if worker is not None:
            worker.run()

    def terminate_worker(self, worker_id: str) -> None:
        worker: Worker = self.workers.get(worker_id, None);
        if worker is not None:
            worker.stop()
        self.workers.pop(worker_id, None)
