"""
This module defines the DelayAction class, an asynchronous action that pauses execution for a specified number of seconds.

DelayAction is designed to introduce a delay in an asynchronous task pipeline, using Python's asyncio.sleep function.
The duration of the delay is configurable via the 'seconds' option.

Decorators:
- @action: Registers DelayAction with the selector "sleep".
- @option: Declares an optional 'seconds' option of type int with a default value.

Usage:
- If 'seconds' is not provided, the default delay is 5 seconds.
"""

from __future__ import annotations

from asyncio import sleep
from typing import Dict, Any

from ..abstracts import Action, TaskContext
from ..decorators import action, option


@action(selector="sleep")
@option(key='seconds', meta_type=int)
class DelayAction(Action):
    """
    An Action that asynchronously delays execution for a given number of seconds.

    This action pauses the task execution for a specified duration before continuing.

    Attributes:
        seconds (int): Number of seconds to delay; defaults to 5 if not specified.

    Behavior:
        - Reads the 'seconds' option from the options dictionary.
        - Awaits asyncio.sleep for the specified duration.
        - Proceeds to the next action in the chain.
    """

    async def run(self, context: TaskContext, options: Dict[str, Any] = {}) -> TaskContext:
        """
        Run the delay asynchronously within the task context.

        Args:
            context (TaskContext): The current task execution context.
            options (Dict[str, Any], optional): A dictionary containing execution options.
                'seconds' (int) specifies how long to sleep. Defaults to 5 if not provided.

        Returns:
            TaskContext: The task context after the delay and continuation.
        """
        seconds = int(options.get('seconds', 5))
        await sleep(seconds)
        return await self.next(context)
