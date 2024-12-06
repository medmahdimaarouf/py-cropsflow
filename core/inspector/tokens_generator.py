import uuid

from common.decorators import ModuleDecoratorMetaData
from common.utils import InjectionToken


def _generate_token(metadata: ModuleDecoratorMetaData) -> InjectionToken:
    return metadata.target.__name__ + "." + uuid.uuid4()
