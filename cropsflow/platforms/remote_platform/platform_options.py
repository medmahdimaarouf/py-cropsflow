from dataclasses import dataclass, field

from cropsflow.core.application_options import ApplicationOptions


@dataclass
class PlatformOptions(ApplicationOptions):
    port: int = field(default_factory=int)
