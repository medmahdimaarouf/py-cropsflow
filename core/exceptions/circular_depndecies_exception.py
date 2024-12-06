class CircularDependenciesException(RuntimeError):
    dep: str
    location: str

    def __init__(self, dep: str, location: str):
        self.dep = dep
        self.location = location
