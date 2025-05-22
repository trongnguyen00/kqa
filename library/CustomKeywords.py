from robotlibcore import DynamicCore
from robot.api.deco import library

from library.CustomTelnet import CustomTelnet
from library.terminal.TopologyLoader import TopologyLoader
from library.utils.TableVerificationLibrary import TableVerificationLibrary
from library.cdr.CDRouterLibrary import CDRouterLibrary
from library.ixia.ixia_library import IxiaLibrary
from library.terminal.dal.keywords.gpon import GponKeywords

@library(scope='GLOBAL')
class CustomKeywords(DynamicCore):
    def __init__(self):
        self.topology_loader = TopologyLoader()  # 👈 gán vào biến để có thể gọi từ bên ngoài

        libraries = [
            self.topology_loader,
            CustomTelnet(),
            TableVerificationLibrary(),
            CDRouterLibrary(),
            IxiaLibrary(),
            GponKeywords()
        ]
        super().__init__(libraries)
