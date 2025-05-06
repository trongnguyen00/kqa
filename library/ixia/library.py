from robot.api.deco import library

from ixia.base import TclBase
from ixia.connection import IxiaConnection
from ixia.port import IxiaPort
from ixia.media import IxiaMedia
from ixia.session import IxiaSession
from ixia.emulation import IxiaEmulation

@library
class IxiaLibrary:
    def __init__(self):
        base = TclBase()
        self.connection = IxiaConnection(base)
        self.port = IxiaPort(base)
        self.media = IxiaMedia(base)
        self.session = IxiaSession(base)
        self.emulation = IxiaEmulation(base)
