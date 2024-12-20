from abc import abstractmethod


class WorkerTreeNode(Generic[T], ABC):
    playbook_item: TaskPlaybookItem
    nodes: List["WorkerTreeNode"]

    def __int__(self, playbook_item: TaskPlaybookItem, parent: "WorkerTreeNode" = None):
        self.playbook_item = playbook_item
        self.nodes = []

    @abstractmethod
    def run(self):
        pass

    def instantiate(self) -> T:
        return self.injector.resolve(scope=InjectionScope.TRANSIENT, optional=False)

    @abstractmethod
    def add_node(self, playbook_item: TaskPlaybookItem):
        pass
