from abc import abstractmethod, ABC
from copy import deepcopy
from threading import Thread, Event
from typing import Callable, List

from cropsflow.common.abstracts import UIDataModel
from .exceptions import ScheduleError
from .jobs import Job, PeriodicJob


def to_milliseconds(ms=0, s=0, m=0, h=0, d=0):
    return ms + s * 1000 + m * 60_000 + h * 3_600_000 + d * 86_400_000


class BaseScheduler(UIDataModel, ABC):

    def __init__(self):
        self.__thread: Thread = Thread(target=self.__run_loop, daemon=True,
                                       name=self.name or 'CropsFlow unnamed scheduler')
        self.__jobs: List[Job] = []
        self.__should_stop: Event = Event()
        self.__should_wakeup: Event = Event()
        self.__is_running: bool = False

    @property
    def jobs(self) -> List[Job]:
        return deepcopy(self.__jobs)

    def every(self, milliseconds: int = 0, seconds: int = 0, minutes: int = 0, hours: int = 0,
              days: int = 0, **args) -> Callable:
        def decorator(target: Callable):
            self.schedule_every(call_back=target,
                                milliseconds=milliseconds, seconds=seconds, minutes=minutes, hours=hours, days=days,
                                **args)
            return target

        return decorator

    def once(self, milliseconds: int = 0, seconds: int = 0, minutes: int = 0, hours: int = 0,
             days: int = 0, **args) -> Callable:
        def decorator(target: Callable):
            self.schedule_once(call_back=target,
                               milliseconds=milliseconds, seconds=seconds, minutes=minutes, hours=hours, days=days,
                               **args)
            return target

        return decorator

    def schedule_every(self, call_back: Callable, milliseconds: int = 0, seconds: int = 0, minutes: int = 0,
                       hours: int = 0, days: int = 0, **args):
        job = PeriodicJob(milliseconds=milliseconds, seconds=seconds, minutes=minutes, hours=hours, days=days,
                          run_once=False, callback=call_back, **args)
        self.__jobs.append(job)
        self.__should_wakeup.set()

    def schedule_once(self, call_back: Callable, milliseconds: int = 0, seconds: int = 0, minutes: int = 0,
                      hours: int = 0, days: int = 0, **args):
        job = PeriodicJob(milliseconds=milliseconds, seconds=seconds, minutes=minutes, hours=hours, days=days,
                          run_once=True, callback=call_back, **args)
        self.__jobs.append(job)
        self.__should_wakeup.set()

    def start(self):
        if self.__is_running:
            raise ScheduleError(f"Scheduler '{self.name}' is already running")
        self.__is_running = True
        self.__thread.start()

    def __run_loop(self):
        while not self.__should_stop.is_set():
            executed_jobs = []

            for job in sorted(self.__jobs):
                if job.should_executed:
                    try:
                        self.execute_job(job)
                        executed_jobs.append(job)
                    except Exception:
                        pass

                    if job.run_once:
                        self.__jobs.remove(job)
                    else:
                        job.update_for_next()
                else:
                    break

            upcoming_jobs = sorted(self.__jobs)
            if upcoming_jobs:
                sleep_duration = max(0, upcoming_jobs[0].timing.remains / 1000)
                self.__should_wakeup.wait(timeout=sleep_duration)
                self.__should_wakeup.clear()
            else:
                self.__should_wakeup.wait()
                self.__should_wakeup.clear()

    def shutdown(self, wait: bool = False):
        if not self.__is_running:
            raise ScheduleError(f"Scheduler '{self.name}' is already shutdown")
        self.__should_stop.set()
        self.__should_wakeup.set()
        if wait:
            self.__thread.join()
        self.__is_running = False

    @abstractmethod
    def execute_job(self, job: Job):
        pass
