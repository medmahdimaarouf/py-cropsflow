from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class TaskPlaybookParseNode:
    selector: str
    options: Dict[str, str] = field(default_factory=dict)
    children: List["TaskPlaybookParseNode"] = field(default_factory=list)
    line: int = field(default_factory=int)


TaskMetaDataParseNode = Dict[str, str]
TaskPlaybookParseTree = List[TaskPlaybookParseNode]
TaskInputSchemaParseTree = Dict[str, str]


@dataclass
class TaskParseTree:
    playbook: TaskPlaybookParseTree = field(default_factory=list)
    metadata: Dict[str, str] = field(default_factory=dict)
    input_schema: None = None

    def __init__(self, meta_data: Dict[str, str], playbook: TaskPlaybookParseTree, dataset: str = None,
                 bucket: str = None):
        self.metadata = meta_data
        self.playbook = playbook
        self.dataset = dataset
        self.bucket = bucket
