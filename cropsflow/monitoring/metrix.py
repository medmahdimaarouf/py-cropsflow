import threading
import time
from collections import defaultdict

from cropsflow.common.abstracts import Metric


class Counter(Metric):
    def __init__(self, name, description=""):
        super().__init__(name, description)
        self._value = 0
        self._lock = threading.Lock()

    def increment(self, amount=1):
        with self._lock:
            self._value += amount

    def collect(self):
        with self._lock:
            return self._value


class Gauge(Metric):
    def __init__(self, name, value_func=None, description=""):
        """
        value_func: function returning current value dynamically
        """
        super().__init__(name, description)
        self._value = 0
        self._lock = threading.Lock()
        self.value_func = value_func

    def set(self, value):
        with self._lock:
            self._value = value

    def collect(self):
        if self.value_func:
            return self.value_func()
        with self._lock:
            return self._value


class Timer(Metric):
    def __init__(self, name, description=""):
        super().__init__(name, description)
        self._count = 0
        self._total_time = 0.0
        self._lock = threading.Lock()

    def record(self, duration_seconds: float):
        with self._lock:
            self._count += 1
            self._total_time += duration_seconds

    def time(self):
        """Context manager to time a code block."""

        class TimerContext:
            def __init__(self, timer):
                self.timer = timer

            def __enter__(self):
                self.start = time.perf_counter()
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                end = time.perf_counter()
                self.timer.record(end - self.start)

        return TimerContext(self)

    def collect(self):
        with self._lock:
            avg = self._total_time / self._count if self._count > 0 else 0
            return {"count": self._count, "total_time": self._total_time, "avg_time": avg}


class Histogram(Metric):
    def __init__(self, name, buckets=None, description=""):
        """
        buckets: list of upper bounds for buckets
        """
        super().__init__(name, description)
        if buckets is None:
            buckets = [0.1, 0.5, 1, 5, 10, float("inf")]
        self.buckets = sorted(buckets)
        self.counts = defaultdict(int)
        self._lock = threading.Lock()

    def observe(self, value):
        with self._lock:
            for bucket in self.buckets:
                if value <= bucket:
                    self.counts[bucket] += 1
                    break

    def collect(self):
        with self._lock:
            return dict(self.counts)


class Summary(Metric):
    def __init__(self, name, description=""):
        super().__init__(name, description)
        self.values = []
        self._lock = threading.Lock()

    def observe(self, value):
        with self._lock:
            self.values.append(value)

    def collect(self):
        with self._lock:
            count = len(self.values)
            if count == 0:
                return {}
            sorted_vals = sorted(self.values)

            def percentile(p):
                k = int(p * count)
                return sorted_vals[min(k, count - 1)]

            return {
                "count": count,
                "min": sorted_vals[0],
                "max": sorted_vals[-1],
                "p50": percentile(0.50),
                "p90": percentile(0.90),
                "p99": percentile(0.99),
                "avg": sum(self.values) / count
            }


class Info(Metric):
    def __init__(self, name, info: dict, description=""):
        super().__init__(name, description)
        self.info = info

    def collect(self):
        return self.info


class BinaryIndicator:
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.state = False

    def set(self, value: bool):
        self.state = value

    def get(self) -> bool:
        return self.state

    def as_int(self) -> int:
        return 1 if self.state else 0

    def __str__(self):
        return f"{self.name}: {'Yes' if self.state else 'No'}"
