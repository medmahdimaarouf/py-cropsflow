from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class TaskPlaybookParseNode:
    selector: str
    options: Dict[str, str] = field(default_factory=dict)
    children: List["TaskPlaybookParseNode"] = field(default_factory=list)
    line: int = field(default_factory=int)


TaskPlaybookParseTree = List[TaskPlaybookParseNode]


@dataclass
class TaskParseTree:
    meta_data: Dict = field(default_factory=dict)
    playbook: TaskPlaybookParseTree = None
    dataset: str = field(default_factory=str)
    bucket: str = field(default_factory=str)

    def __init__(self, meta_data: Dict[str, str], playbook: TaskPlaybookParseTree, dataset: str = None,
                 bucket: str = None):
        self.meta_data = meta_data
        self.playbook = playbook
        self.dataset = dataset
        self.bucket = bucket
