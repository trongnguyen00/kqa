from robotlibcore import DynamicCore
from robot.api.deco import library

from library.CustomTelnet import *
from library.terminal.TopologyLoader import TopologyLoader
from library.utils.TableVerificationLibrary import TableVerificationLibrary
from library.cdr.CDRouterLibrary import CDRouterLibrary
from library.ixia.ixia_library import IxiaLibrary
from library.terminal.dal.keywords.gpon import GponKeywords
from library.terminal.dal.keywords.system import SystemKeywords

@library(scope='GLOBAL')
class CustomKeywords(DynamicCore):
    def __init__(self):
        self.topology_loader = TopologyLoader()
        self.custom_telnet = CustomTelnet()
        self.telnet_group_handler = TelnetCommandGroupHandler(self.custom_telnet)

        libraries = [
            self.topology_loader,
            self.custom_telnet,
            self.telnet_group_handler,
            CustomTelnetConnection(),
            TableVerificationLibrary(),
            CDRouterLibrary(),
            IxiaLibrary(),
            GponKeywords(),
            SystemKeywords()
        ]
        super().__init__(libraries)
