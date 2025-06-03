from dataclasses import dataclass, field

from cropsflow.platforms import ApplicationOptions


@dataclass
class PlatformOptions(ApplicationOptions):
    port: int = field(default_factory=int)
