from typing import Type, Any

from .application import Application
from .application_options import ApplicationOptions
from .application_platform import ApplicationPlatform


class StaticPlatform(ApplicationPlatform):

    async def start(self, t: Type[Any], options: ApplicationOptions = ApplicationOptions(), args: list[str] = []) -> Application:
        return await self.init(t, options=options, overrides=[])


CropsFlow = StaticPlatform()
