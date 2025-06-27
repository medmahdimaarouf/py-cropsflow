from dataclasses import dataclass, field

from cropsflow.core.application_options import ApplicationOptions


@dataclass
class PlatformOptions(ApplicationOptions):
    port: int = field(default_factory=int)
    allow_origins: list = field(default_factory=list)
    allow_credentials: list = field(default_factory=list),
    allow_methods: list = field(default_factory=list),
    allow_headers: list = field(default_factory=list),
