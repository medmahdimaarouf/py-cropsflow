from .task_build_exception import TaskBuildException


class UnknownOptionException(TaskBuildException):
    def __init__(self, name: str, node_name: str, template_file_path: str, line: int, column: int = None) -> None:
        super().__init__(
            message=f"{template_file_path}\n'{name}' is not a known option for '{node_name}' at line : {line}",
            template_file_path=template_file_path, line=line, column=column
        )
