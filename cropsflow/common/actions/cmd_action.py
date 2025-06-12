"""
This module defines the CMDAction class, a specialized Action that executes shell commands asynchronously.

CMDAction uses Python's subprocess module to run the specified shell command provided via options,
captures its standard output, and stores the result internally. It integrates with an asynchronous
task execution framework by implementing the run method and supports chaining to subsequent actions.

Key Features:
- Executes shell commands safely with error handling.
- Captures and stores command output for further processing.
- Designed to work within an async task pipeline with context propagation.

Decorators:
- @action: Registers CMDAction with the selector "cmd".
- @option: Declares a required 'command' option of type str.

Raises:
- Handles subprocess.CalledProcessError and generic exceptions gracefully,
  returning the current task context on errors.
"""

from typing import Dict, Any
import subprocess
from ..abstracts import Action, TaskContext
from ..decorators import action, option


@action(selector="cmd")
@option(key='command', meta_type=str, required=True)
class CMDAction(Action):
    """
    An Action that executes a shell command asynchronously.

    This class runs a shell command specified by the 'command' option using subprocess.run,
    captures the command's standard output, trims it, and stores it as the action's data.

    Attributes:
        command (str): The shell command to be executed, provided in options.

    Behavior:
        - Executes the command asynchronously.
        - On success, stores the trimmed stdout output.
        - On failure (e.g. command error), returns the current task context unchanged.

    Usage:
        Requires the 'command' option to be set with a valid shell command string.
    """

    async def run(self, context: TaskContext, options: Dict[str, Any] = {}) -> TaskContext:
        """
        Execute the shell command asynchronously within the task context.

        Args:
            context (TaskContext): The current task execution context.
            options (Dict[str, Any], optional): A dictionary containing execution options.
                Must include 'command' key with the shell command string.

        Returns:
            TaskContext: The next task context after execution or the current context on error.

        Raises:
            subprocess.CalledProcessError: Handled internally if the command fails.
            Exception: Catches all other exceptions to prevent task interruption.
        """
        try:
            command: str = options.get("command")
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                check=True
            )
            return await self.next(context)
        except subprocess.CalledProcessError:
            return context
        except Exception:
            return context
