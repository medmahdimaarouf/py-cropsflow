class TaskBuildException(RuntimeError):
    template_file_path: str
    line: int
    column: int
    message: str

    def __init__(self, message: str, template_file_path: str, line: int, column: int = None) -> None:
        super(TaskBuildException)
        self.template_file_path = template_file_path
        self.line = line
        self.column = column
        self.message = message
