from cropsflow.common import Init
from cropsflow.common.decorators import module, inject
from cropsflow.router import Router
from cropsflow.platforms import Application
from .data_sources_register import DataSourcesRegister
from .routers import get_data_sources_router


@module(
    providers=[DataSourcesRegister],
    exports=[DataSourcesRegister]
)
class DataModule(Init):
    @inject(arg_name='application', token=Application, optional=False)
    @inject(arg_name='router', token=Router, optional=True)
    async def init(self, application: Application, router: Router) -> None:
        if router is not None:
            data_sources_router: Router = Router(prefix='/data')

            data_sources_router.include_router(router=get_data_sources_router(application=application))

            router.include_router(router=data_sources_router)
