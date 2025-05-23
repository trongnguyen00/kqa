from robot.libraries.BuiltIn import BuiltIn
from library.CustomTelnet import CustomTelnet

class SystemBase:
    """Implementation of System feature"""
    
    def __init__(self):
        self.telnet = BuiltIn().get_library_instance("CustomTelnet")

class SystemDasan1(SystemBase):
    """Implementation of System feature for Dasan V5812G"""
    
    def set_terminal_length(self, line_limit):
        command = f"terminal length {line_limit}"
        return self.telnet.send_command(command)
    
    

class SystemHuawei1(SystemBase):
    """Implementation of System feature for MA5800-X7"""
    
    def set_terminal_length(self, line_limit):
        if line_limit == 0:
            line_limit = 512
        command = f"scroll {line_limit}"
        return self.telnet.send_command(command)
    
    def unset_interactive(self):
        command = f"undo smart"
        return self.telnet.send_command(command)
    
    def set_interactive(self):
        command = f"interactive"
        return self.telnet.send_command(command)