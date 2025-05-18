from .task_build_exception import TaskBuildException


class UnknownNodeSelectorException(TaskBuildException):
    def __init__(self, node_name: str, template_file_path: str, line: int, column: int = None) -> None:
        super().__init__(
            template_file_path=template_file_path, line=line, column=column,
            message=f"{template_file_path}\nNo action or pipe found by selector '{node_name}' at line : {line}"
        )
