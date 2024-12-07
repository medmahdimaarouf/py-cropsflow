from common import PrxModule
from core.application_factory import ApplicationFactory


@PrxModule(
    declarations=[],
    imports=[],
    providers=[],
    exports=[]
)
class AppModule:
    pass


f = ApplicationFactory()
app = f.init(AppModule)
