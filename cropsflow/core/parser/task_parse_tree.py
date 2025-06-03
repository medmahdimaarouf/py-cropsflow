from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class ParseNode:
    line: int = field(default_factory=int)
    source: str = field(default_factory=str)
    column: int = field(default_factory=int)
    template_file_name: str = field(default_factory=str)


@dataclass
class PlaybookParseNode(ParseNode):
    selector: str = field(default_factory=str)
    options: Dict[str, str] = field(default_factory=dict)
    children: List["PlaybookParseNode"] = field(default_factory=list)


TaskPlaybookParseTree = PlaybookParseNode
TaskMetaDataParseNode = Dict[str, str]
TaskInputSchemaParseTree = Dict[str, str]


@dataclass
class TaskParseTree:
    playbook: TaskPlaybookParseTree = None
    metadata: Dict[str, str] = field(default_factory=dict)
    input_schema: None = None

    def __init__(self, meta_data: Dict[str, str], playbook: TaskPlaybookParseTree):
        self.metadata = meta_data
        self.playbook = playbook
        self.input_schema = None
