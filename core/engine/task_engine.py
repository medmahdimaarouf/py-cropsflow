from typing import List, Type

from .task_worker import TaskWorker
from ..injector import Task
from ..application import Application
from .task_builder import build_task


class Engine:
    application: Application
    workers: List[TaskWorker]

    def __init__(self, application: Application):
        self.application = application
        self.workers = []

    async def run(self, meta_type: Type):
        task = self.application.task(meta_type)
        template = build_task(task)
        worker = TaskWorker(playbook=template.playbook)
        self.workers.append(worker)
        await worker.run()
