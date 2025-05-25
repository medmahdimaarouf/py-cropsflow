from dataclasses import dataclass, field


@dataclass
class WorkerModel:
    id: str = field(default_factory=str)
