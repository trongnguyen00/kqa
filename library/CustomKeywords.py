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
    """Custom Keywords library that combines various test automation libraries.
    
    This library provides access to:
    - Telnet connection management and command execution
    - Topology loading and device information
    - Table verification utilities
    - CDRouter testing capabilities
    - Ixia testing capabilities
    - GPON and System specific keywords
    """
    
    def __init__(self):
        """Initialize the library with all required components."""
        # Initialize core components
        self.topology_loader = TopologyLoader()
        self.custom_telnet = CustomTelnet()

        # Initialize all libraries
        libraries = [
            self.topology_loader,
            self.custom_telnet,
            TableVerificationLibrary(),
            CDRouterLibrary(),
            IxiaLibrary(),
            GponKeywords(),
            SystemKeywords()
        ]
        super().__init__(libraries)
