from robotlibcore import DynamicCore
from robot.api.deco import library
from ixia.base import TclBase
from ixia.keywords.connection import ConnectionKeywords
from ixia.keywords.session import SessionKeywords
from ixia.keywords.port import PortKeywords
from ixia.keywords.media import MediaKeywords
from ixia.keywords.linklayer import LinkLayerKeywords

@library
class IxiaLibrary(DynamicCore):
    def __init__(self):
        base = TclBase()
        libraries = [
            ConnectionKeywords(base),
            SessionKeywords(base),
            PortKeywords(base),
            MediaKeywords(base),
            LinkLayerKeywords(base)
        ]
        super().__init__(libraries)