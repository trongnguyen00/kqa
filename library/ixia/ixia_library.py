from robotlibcore import DynamicCore
from robot.api.deco import library
from library.ixia.base import TclBase
from library.ixia.keywords.connection import ConnectionKeywords
from library.ixia.keywords.session import SessionKeywords
from library.ixia.keywords.port import PortKeywords
from library.ixia.keywords.media import MediaKeywords
from library.ixia.keywords.linklayer import LinkLayerKeywords
from library.ixia.keywords.trafficprofile import TrafficProfileKeywords
from library.ixia.keywords.traffictest import TrafficTestKeywords

@library
class IxiaLibrary(DynamicCore):
    def __init__(self):
        base = TclBase()
        libraries = [
            ConnectionKeywords(base),
            SessionKeywords(base),
            PortKeywords(base),
            MediaKeywords(base),
            LinkLayerKeywords(base),
            TrafficProfileKeywords(base),
            TrafficTestKeywords(base)
        ]
        super().__init__(libraries)