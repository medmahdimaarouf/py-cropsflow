from core.engine import TaskWorker, build_task
from core.injector import Task


class TaskWorkerFactory:

    @staticmethod
    def create_worker(task: Task) -> TaskWorker:
        return TaskWorker(playbook=build_task(task=task))