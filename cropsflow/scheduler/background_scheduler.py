import traceback
from concurrent.futures import ThreadPoolExecutor

from .base_scheduler import BaseScheduler
from .jobs import Job


class BackgroundScheduler(BaseScheduler):
    def __init__(self, max_workers: int = 4):
        super().__init__()
        self.__executor = ThreadPoolExecutor(max_workers=max_workers)

    def execute_job(self, job: Job):
        def job_wrapper():
            try:
                return job.execute()
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)

        self.__executor.submit(job_wrapper)
