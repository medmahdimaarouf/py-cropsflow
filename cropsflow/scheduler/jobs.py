import time
from dataclasses import dataclass, field
from typing import Callable, Any, Dict, Optional
from enum import Enum, auto

from .exceptions import IntervalError


def now_ms() -> int:
    """Get current time in milliseconds since epoch"""
    return int(time.time() * 1000)


class JobState(Enum):
    """Enumeration of possible job states"""
    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()


@dataclass
class JobTiming:
    interval: int  # in milliseconds
    starting_from: int = field(default_factory=now_ms)
    last_executed: int = field(default=0, init=False)

    @property
    def remains(self) -> int:
        """Returns milliseconds until next execution"""
        next_run = self.starting_from + self.interval
        return max(0, next_run - now_ms())

    @property
    def is_due(self) -> bool:
        """Returns True if the job is due to run"""
        return now_ms() >= (self.starting_from + self.interval)

    def __lt__(self, other: 'JobTiming') -> bool:
        """Comparison based on remaining time"""
        return self.remains < other.remains

    def __str__(self) -> str:
        return (f"JobTiming(interval={self.interval}ms, "
                f"next_run={time.strftime('%Y-%m-%d %H:%M:%S', time.localtime((self.starting_from + self.interval)/1000))}, "
                f"remains={self.remains}ms)")


class Job:
    """Base class for all job types"""

    def __init__(self, timing: JobTiming, callback: Callable, run_once: bool = False, **kwargs):
        if timing.interval <= 0:
            raise IntervalError(f"Invalid interval provided for job: {timing.interval}")

        self._timing: JobTiming = timing
        self._callback: Callable = callback
        self._callback_kwargs: Dict[str, Any] = kwargs
        self.run_once: bool = run_once
        self.state: JobState = JobState.PENDING
        self.execution_count: int = 0
        self.last_error: Optional[Exception] = None

    def __lt__(self, other: 'Job') -> bool:
        """Comparison based on timing"""
        return self._timing < other._timing

    @property
    def timing(self) -> JobTiming:
        return self._timing

    @property
    def should_execute(self) -> bool:
        """Returns True if the job should be executed now"""
        return self._timing.is_due and self.state != JobState.RUNNING

    def update_for_next(self) -> None:
        """Update timing for the next execution"""
        if not self.run_once:
            self._timing.starting_from = now_ms()
            self.state = JobState.PENDING
        else:
            self.state = JobState.COMPLETED

    def execute(self) -> Any:
        """Execute the job's callback function"""
        self.state = JobState.RUNNING
        try:
            result = self._callback(**self._callback_kwargs)
            self.state = JobState.COMPLETED
            self.execution_count += 1
            self._timing.last_executed = now_ms()
            return result
        except Exception as e:
            self.state = JobState.FAILED
            self.last_error = e
            raise

    def __str__(self) -> str:
        return (f"Job(callback={self._callback.__name__}, "
                f"interval={self._timing.interval}ms, "
                f"state={self.state.name}, "
                f"run_once={self.run_once})")


class PeriodicJob(Job):
    """Job that runs periodically at fixed intervals"""

    def __init__(self, callback: Callable,
                 milliseconds: int = 0,
                 seconds: int = 0,
                 minutes: int = 0,
                 hours: int = 0,
                 days: int = 0,
                 run_once: bool = False,
                 **kwargs):
        interval = (
                milliseconds +
                seconds * 1000 +
                minutes * 60 * 1000 +
                hours * 60 * 60 * 1000 +
                days * 24 * 60 * 60 * 1000
        )
        super().__init__(
            timing=JobTiming(interval=interval),
            callback=callback,
            run_once=run_once,
            **kwargs
        )


class DailyJob(PeriodicJob):
    """Job that runs daily at the same time"""

    def __init__(self, days: int = 1, callback: Callable = None, **kwargs):
        if days <= 0:
            raise IntervalError("Days must be positive")
        super().__init__(
            days=days,
            callback=callback,
            **kwargs
        )


class WeeklyJob(PeriodicJob):
    """Job that runs weekly on the same day/time"""

    def __init__(self, weeks: int = 1, callback: Callable = None, **kwargs):
        if weeks <= 0:
            raise IntervalError("Weeks must be positive")
        super().__init__(
            days=weeks * 7,
            callback=callback,
            **kwargs
        )