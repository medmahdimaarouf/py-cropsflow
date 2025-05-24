from dataclasses import dataclass, field


@dataclass
class ApplicationOptions:
    debug: bool = field(default=False)
