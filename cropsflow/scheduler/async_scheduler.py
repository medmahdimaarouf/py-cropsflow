import asyncio
import traceback
from asyncio import AbstractEventLoop
from typing import Optional

from .base_scheduler import BaseScheduler
from .jobs import Job


class AsyncScheduler(BaseScheduler):
    def __init__(self, event_loop: Optional[AbstractEventLoop] = None):
        super().__init__()
        self.__event_loop: AbstractEventLoop = event_loop or asyncio.get_event_loop()

    def execute_job(self, job: Job):
        async def wrap():
            return job.execute()

        try:
            if self.__event_loop.is_running():
                return asyncio.run_coroutine_threadsafe(wrap(), self.__event_loop)
            else:
                return self.__event_loop.run_until_complete(wrap())

        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
