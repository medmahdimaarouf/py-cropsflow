import uuid

from cropsflow.common.decorators import ModuleDecoratorMetaData
from cropsflow.common.utils import InjectionToken


def generate_token(metadata: ModuleDecoratorMetaData) -> InjectionToken:
    return metadata.target.__name__ + "." + uuid.uuid4()
