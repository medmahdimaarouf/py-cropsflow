from dataclasses import dataclass, field
from typing import Dict, List

TaskTemplateMetaData = Dict[str, str]
TaskPlaybook = List[dict]


@dataclass
class TaskTemplate:
    dataset: str
    meta_data: TaskTemplateMetaData = field(default_factory=dict)
    playbook: TaskPlaybook = field(default_factory=list)

    def __init__(self, meta_data: Dict[str, str], playbook: List[dict], dataset: str = None):
        self.meta_data = meta_data
        self.playbook = playbook
        self.dataset = dataset
