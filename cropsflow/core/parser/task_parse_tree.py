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
    playbook: TaskPlaybookParseTree = field(default=None)
    metadata: Dict[str, str] = field(default_factory=dict)
    input_schema: None = field(default=None)
