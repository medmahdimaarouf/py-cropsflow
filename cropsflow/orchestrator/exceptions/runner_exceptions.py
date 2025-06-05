import inspect
import sys

import traceback


def print_traceback_from_frame_of(user_method, exc: BaseException):
    target_code = user_method.__func__.__code__  # Code object of the method
    tb = exc.__traceback__
    selected_tb = None

    # Walk through traceback to find the frame matching the user's method
    while tb is not None:
        if tb.tb_frame.f_code is target_code:
            selected_tb = tb
            break
        tb = tb.tb_next

    if selected_tb:
        traceback.print_tb(selected_tb)
        print(f"ERROR : {exc.__str__()}", file=sys.stderr)
    else:
        traceback.print_tb(exc.__traceback__)


class RunnerException(Exception):
    def print_full_traceback(self):
        traceback.print_tb(self.__traceback__)

    def print_partial_traceback(self):
        from cropsflow.orchestrator.runner import Runner
        runner_class_path: str = inspect.getfile(Runner)
        traceback_partial_index: int = 0
        for t in traceback.extract_tb(self.__traceback__):
            print(t.filename)
            if t.filename == runner_class_path:
                break
            else:
                traceback_partial_index = traceback_partial_index + 1
        traceback.print_stack()
