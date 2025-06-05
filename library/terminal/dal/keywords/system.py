from robot.api.deco import keyword
from library.terminal.dal.feature_loader import FeatureLoader

class SystemKeywords:

    def __init__(self):
        self._system = None

    @property
    def system(self):
        if not self._system:
            self._system = FeatureLoader("system").load()
        return self._system

    @keyword
    def set_terminal_length(self, line_limit=0):
        return self.system.set_terminal_length(line_limit)

    @keyword
    def unset_interactive(self):
        """keyword using for huawei only, it should perform with each test"""
        return self.system.unset_interactive()
    
    @keyword
    def set_interactive(self):
        """keyword using for huawei only, to enable again smart command mode. it don't suggest to using during test by it make some false hanle"""
        return self.system.set_interactive()
    