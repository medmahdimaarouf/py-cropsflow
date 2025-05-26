from dataclasses import dataclass, field
from datetime import time


@dataclass
class WorkerDetailsResponse:
    id: str = field(default_factory=str)
    task_title: str = field(default_factory=str)
    task_description: str = field(default_factory=str)
    task_container_id: str = field(default_factory=str)
    is_running: bool = field(default_factory=bool)
    start_time: time = field(default_factory=time)
