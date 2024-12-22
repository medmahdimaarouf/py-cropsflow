from .task_builder import TaskPlaybook, build_task
from ..injector import Task


class TaskWorker:
    playbook: TaskPlaybook

    def __init__(self, playbook: TaskPlaybook):
        self.playbook = playbook

    async def run(self):
        for playbook_node in self.playbook:
            await playbook_node.run()


class TaskWorkerFactory:

    @staticmethod
    def create_worker(task: Task) -> TaskWorker:
        return TaskWorker(playbook=build_task(task=task))
