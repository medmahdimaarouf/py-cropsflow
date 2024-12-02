from .metadata_scanner import *
from ..injector import Container


class Scanner(object):
    container: Container

    def __init__(self, container: Container):
        self.container = container

    
