from typing import Dict, Any

from .container import Container
from common.decorators import ActionDecoratorMetaData, InjectionScope
from common.abstracts import Action as BaseAction, Init


class Action(Container):
    def __int__(self, metadata: ActionDecoratorMetaData, host: Container):
        super().__init__(metadata=metadata, host=host)

    async def run(self, binding: Dict[str, Any] = {}):
        instance: BaseAction = self.injector.resolve(scope=InjectionScope.TRANSIENT)
        if isinstance(instance, Init):
            instance.init()
        print("Running ActionWorkerNode ")
        await instance.run(context=None)
