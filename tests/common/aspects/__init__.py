from common.aspects import after
from cropsflow.common.aspects import before


class MyClass:

    def method(self, *args):
        print("method call original args", args, self.__class__.__name__)
        return 'OK'


instance = MyClass()


@before(target=MyClass.method)
def aspect_before(*args):
    print(['Before'])


@after(target=MyClass.method)
def aspect_after(*args):
    print(['After'])


instance.method(1, 2)
