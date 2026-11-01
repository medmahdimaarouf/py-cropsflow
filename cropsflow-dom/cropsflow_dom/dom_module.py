from cropsflow.common.decorators import module

from cropsflow_dom.html_dom.module import HTMLModule
from cropsflow_dom.xml_dom.xml_module import XMLModule


@module(
    imports=[HTMLModule, XMLModule],
    exports=[HTMLModule, XMLModule]
)
class DOMModule:
    pass
