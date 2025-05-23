from robotlibcore import DynamicCore
from robot.api.deco import library

from library.CustomTelnet import CustomTelnet
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

        libraries = [
            self.topology_loader,
            CustomTelnet(),
            TableVerificationLibrary(),
            CDRouterLibrary(),
            IxiaLibrary(),
            GponKeywords(),
            SystemKeywords()
        ]
        super().__init__(libraries)
