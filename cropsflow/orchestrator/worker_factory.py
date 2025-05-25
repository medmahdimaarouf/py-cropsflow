from cropsflow.orchestrator import Worker, build_task
from cropsflow.core.injector import Task


class TaskWorkerFactory:

    @staticmethod
    def create_worker(task: Task) -> Worker:
        return Worker(playbook=build_task(task=task))
