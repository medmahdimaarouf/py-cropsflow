import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable, Optional

from scheduler.exceptions import IntervalError


def now_ms() -> int:
    return int(time.time() * 1000)


@dataclass
class JobTiming:
    interval: int
    starting_from: int = field(default_factory=now_ms)

    @property
    def remains(self) -> int:
        now_ms() - (self.starting_from + self.interval)

    def __lt__(self, other: 'JobTiming'):
        return self.remains < other.remains

    def __str__(self):
        return f"Job timing interval: {self.interval * 100}s starting from " \
               f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.starting_from / 1000))}"


class Job:

    def __init__(self, timing: JobTiming, callback: Callable, run_once: bool = True, **args):
        if timing.interval <= 0:
            raise IntervalError(f"Invalid interval provided for job: {timing.interval}")
        self.__timing: JobTiming = timing  # job timing
        self.__callback: Callable = callback  # function will be handled when scheduler trigger
        self.__callback_args = args
        self.run_once = run_once

    def __lt__(self, other: 'Job'):
        return self.__timing < other.__timing

    @property
    def should_executed(self) -> bool:
        return self.__timing.remains <= 0

    def update_for_next(self):
        self.__timing.starting_from = now_ms()

    def execute(self):
        return self.__callback(**self.__callback_args)


class PeriodicJob(Job):

    def __init__(self, callback: Callable,
                 milliseconds: int = 0,
                 seconds: int = 0,
                 minutes: int = 0,
                 hours: int = 0,
                 days: int = 0, **args):
        super().__init__(interval=JobTiming(interval=(
                milliseconds +
                seconds * 1000 +
                minutes * 60 * 1000 +
                hours * 60 * 60 * 1000 +
                days * 24 * 60 * 60 * 1000
        )), callback=callback, **args)

    def __lt__(self, other: 'Job'):
        return self.__interval < other.interval


class DalyJob(PeriodicJob):

    def __init__(self, days: int, callback: Callable, **args):
        super().__init__(days=days, callback=callback, **args)


class WeeklyJob(PeriodicJob):

    def __init__(self, weeks: int, callback: Callable, **args):
        super().__init__(days=weeks * 7, callback=callback, **args)
