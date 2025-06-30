from abc import abstractmethod, ABC
from copy import deepcopy
from threading import Thread, Event, Condition
from typing import Callable, List, Optional, Dict, Any
import time
import logging

from cropsflow.common.abstracts import UIDataModel
from .exceptions import ScheduleError
from .jobs import Job, PeriodicJob, JobState


def now_ms() -> int:
    """Get current time in milliseconds since epoch"""
    return int(time.time() * 1000)


def to_milliseconds(ms=0, s=0, m=0, h=0, d=0) -> int:
    """Convert time units to milliseconds"""
    return ms + s * 1000 + m * 60_000 + h * 3_600_000 + d * 86_400_000


class BaseScheduler(UIDataModel, ABC):
    """
    Base scheduler class that manages and executes jobs at specified intervals.
    Subclasses must implement the execute_job method to define how jobs are run.
    """

    def __init__(self):
        self.__thread: Optional[Thread] = None
        self.__jobs: List[Job] = []
        self.__should_stop = Event()
        self.__wakeup_condition = Condition()
        self.__is_running: bool = False
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    @property
    def jobs(self) -> List[Job]:
        """Return a copy of the current job list"""
        return deepcopy(self.__jobs)

    def schedule_every(self, call_back: Callable, milliseconds: int = 0, seconds: int = 0,
                       minutes: int = 0, hours: int = 0, days: int = 0, **kwargs) -> Job:
        """
        Schedule a recurring job that runs at fixed intervals.

        Args:
            call_back: The function to execute
            milliseconds: Time in milliseconds
            seconds: Time in seconds
            minutes: Time in minutes
            hours: Time in hours
            days: Time in days
            kwargs: Additional arguments to pass to the callback

        Returns:
            The created Job instance
        """
        job = PeriodicJob(
            callback=call_back,
            milliseconds=milliseconds,
            seconds=seconds,
            minutes=minutes,
            hours=hours,
            days=days,
            run_once=False,
            **kwargs
        )
        with self.__wakeup_condition:
            self.__jobs.append(job)
            self.__wakeup_condition.notify()
        return job

    def schedule_once(self, call_back: Callable, milliseconds: int = 0, seconds: int = 0,
                      minutes: int = 0, hours: int = 0, days: int = 0, **kwargs) -> Job:
        """
        Schedule a one-time job that runs after the specified delay.

        Args:
            call_back: The function to execute
            milliseconds: Time in milliseconds
            seconds: Time in seconds
            minutes: Time in minutes
            hours: Time in hours
            days: Time in days
            kwargs: Additional arguments to pass to the callback

        Returns:
            The created Job instance
        """
        job = PeriodicJob(
            callback=call_back,
            milliseconds=milliseconds,
            seconds=seconds,
            minutes=minutes,
            hours=hours,
            days=days,
            run_once=True,
            **kwargs
        )
        with self.__wakeup_condition:
            self.__jobs.append(job)
            self.__wakeup_condition.notify()
        return job

    def start(self) -> None:
        """Start the scheduler thread"""
        if self.__is_running:
            raise ScheduleError(f"Scheduler '{self.name}' is already running")

        self.__should_stop.clear()
        self.__thread = Thread(
            target=self.__run_loop,
            daemon=False,
            name=self.name or 'CropsFlow unnamed scheduler'
        )
        self.__is_running = True
        self.__thread.start()
        self.logger.info(f"Scheduler '{self.name}' started")

    def shutdown(self, wait: bool = False) -> None:
        """
        Stop the scheduler.

        Args:
            wait: If True, wait for the scheduler thread to complete
        """
        if not self.__is_running:
            raise ScheduleError(f"Scheduler '{self.name}' is already shutdown")

        self.logger.info(f"Shutting down scheduler '{self.name}'")
        self.__should_stop.set()

        with self.__wakeup_condition:
            self.__wakeup_condition.notify_all()

        if wait and self.__thread is not None:
            self.__thread.join(timeout=5.0)
            if self.__thread.is_alive():
                self.logger.warning("Scheduler thread did not stop gracefully")

        self.__is_running = False
        self.logger.info(f"Scheduler '{self.name}' stopped")

    def __run_loop(self) -> None:
        """Main scheduler loop that manages job execution"""
        self.logger.debug("Scheduler loop started")

        while not self.__should_stop.is_set():
            try:
                current_time = now_ms()
                jobs_to_remove = []
                # Process all jobs that are ready to run
                for job in sorted(self.__jobs):
                    if self.__should_stop.is_set():
                        break

                    if job.should_execute:
                        try:
                            self.execute_job(job)
                            job.update_for_next()

                            if job.run_once:
                                jobs_to_remove.append(job)
                        except Exception as e:
                            self.logger.error(
                                f"Error executing job {job}: {str(e)}",
                                exc_info=True
                            )
                            job.state = JobState.FAILED
                            job.last_error = e

                # Remove completed one-time jobs
                if jobs_to_remove:
                    with self.__wakeup_condition:
                        self.__jobs = [j for j in self.__jobs if j not in jobs_to_remove]

                # Calculate sleep time until next job is due
                sleep_time = 1.0  # Default sleep if no jobs
                if self.__jobs:
                    next_job = min(self.__jobs, key=lambda j: j.timing.remains)
                    sleep_time = max(0.001, next_job.timing.remains / 1000.0)

                # Sleep until next job or wakeup signal
                with self.__wakeup_condition:
                    if not self.__should_stop.is_set():
                        self.__wakeup_condition.wait(timeout=sleep_time)
            except Exception as e:
                self.logger.error(f"Unexpected error in scheduler loop: {str(e)}", exc_info=True)
                time.sleep(1.0)  # Prevent tight error loops

        self.logger.debug("Scheduler loop exiting")

    def every(self, milliseconds: int = 0, seconds: int = 0, minutes: int = 0,
              hours: int = 0, days: int = 0, **kwargs) -> Callable:
        """
        Decorator for scheduling recurring jobs.

        Example:
            @scheduler.every(seconds=30)
            def my_job():
                print("Running every 30 seconds")
        """

        def decorator(target: Callable) -> Callable:
            self.schedule_every(
                call_back=target,
                milliseconds=milliseconds,
                seconds=seconds,
                minutes=minutes,
                hours=hours,
                days=days,
                **kwargs
            )
            return target

        return decorator

    def once(self, milliseconds: int = 0, seconds: int = 0, minutes: int = 0,
             hours: int = 0, days: int = 0, **kwargs) -> Callable:
        """
        Decorator for scheduling one-time jobs.

        Example:
            @scheduler.once(minutes=5)
            def my_job():
                print("Running once after 5 minutes")
        """

        def decorator(target: Callable) -> Callable:
            self.schedule_once(
                call_back=target,
                milliseconds=milliseconds,
                seconds=seconds,
                minutes=minutes,
                hours=hours,
                days=days,
                **kwargs
            )
            return target

        return decorator

    def remove_job(self, job: Job) -> bool:
        """
        Remove a job from the scheduler.

        Args:
            job: The job to remove

        Returns:
            True if the job was found and removed, False otherwise
        """
        with self.__wakeup_condition:
            try:
                self.__jobs.remove(job)
                return True
            except ValueError:
                return False

    @abstractmethod
    def execute_job(self, job: Job) -> Any:
        """
        Abstract method that defines how jobs are executed.
        Must be implemented by subclasses.

        Args:
            job: The job to execute

        Returns:
            The result of the job execution (if any)
        """
        pass
