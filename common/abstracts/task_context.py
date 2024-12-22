from typing import Optional, Any

from .logger import Logger


class TaskContext:
    parent: Optional['TaskContext'] = None
    logger: Optional[Logger] = None
    data: Any = None

    def __init__(self, parent: Optional['TaskContext'] = None, logger: Optional[Logger] = None):
        self.parent = parent
        self.data = None
        self.logger = logger  # if logger else Logger()
