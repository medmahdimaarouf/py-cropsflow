"""
This module defines the IterateAction class, which processes each element
in a provided list by invoking the next action for each item asynchronously.

IterateAction is designed to loop over an iterable provided via the 'of' option,
and for each element, it calls the next action in the pipeline.

Decorators:
- @action: Registers IterateAction with the selector "iterate".
- @option: Declares a required 'of' option expected to be a list.

Usage:
- The 'of' option must be provided as a list to iterate over.
"""

from typing import Iterable, Any, List, Dict, Optional

from ..abstracts import Action, TaskContext
from ..decorators import action, option


@action(selector="iterate")
@option(key='of', meta_type=List, required=True)
class IterateAction(Action):
    """
    An Action that iterates over a list of items and executes subsequent actions for each item.

    Attributes:
        of (List[Any]): The list of items to iterate over, passed as an option.
    """

    def __init__(self):
        super().__init__()
        self.of: Iterable[Any] = []

    async def run(self, context: TaskContext, options: Optional[Dict[str, Any]] = None) -> TaskContext:
        """
        Iterate over the provided list and invoke the next action for each element.

        Args:
            context (TaskContext): The current task execution context.
            options (Dict[str, Any], optional): Options dictionary expected to contain 'of' as a list.

        Returns:
            TaskContext: The task context after iteration is complete.
        """
        options = options or {}
        self.of = options.get('of', [])
        for item in self.of:
            context.data = item
            await self.next(context)
        return context
