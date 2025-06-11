from typing import Type, Union

from cropsflow.common.decorators import service, InjectionScope
from cropsflow.core import Injector
from cropsflow.core.builder import *
from .runner import PlayBookRunner
from .worker import Worker
from .workers_queue import WorkersQueue
from .workers_scheduler import WorkersScheduler


@service(scope=InjectionScope.DEFAULT)
class Orchestrator:
    container: Container
    pool: Dict[str, Worker] = {}
    queue: WorkersQueue = WorkersQueue()
    scheduler: WorkersScheduler = WorkersScheduler()

    def __init__(self, injector: Injector):
        self.container = injector.container
        self.pool = {}
        self.queue = WorkersQueue()
        self.scheduler = WorkersScheduler()

    def create_worker(self, meta_type: Type) -> Worker:
        task: Container = self.container.get_task(meta_type)
        if task is None:
            raise Exception(f'Unknown task class {meta_type.__name__}')
        template = TaskTemplateBuilder(task=task).build()
        worker = Worker(runner=PlayBookRunner(node=template.playbook))
        self.pool[worker.id] = worker
        return worker

    def get_worker(self, worker_id: str) -> Union[Worker, None]:
        return self.pool.get(worker_id, None)

    def start_worker(self, worker_id: str) -> None:
        worker: Worker = self.pool.get(worker_id, None);
        if worker is not None:
            worker.run()

    def terminate_worker(self, worker_id: str) -> None:
        worker: Worker = self.pool.get(worker_id, None);
        if worker is not None:
            worker.stop()
        self.pool.pop(worker_id, None)
