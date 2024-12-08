from common import PrxModule, CommonModule
from core.application_factory import ApplicationFactory


@PrxModule(
    declarations=[],
    imports=[CommonModule],
    providers=[],
    exports=[]
)
class AppModule:
    pass


def start():
    f = ApplicationFactory()
    app = f.init(AppModule)


if __name__ == '__main__':
    start()
