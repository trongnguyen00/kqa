from robot.libraries.BuiltIn import BuiltIn
from library.CustomTelnet import CustomTelnet

class TerminalBase:
    """Implementation of Terminal feature"""
    
    def __init__(self):
        self.telnet = BuiltIn().get_library_instance("CustomKeywords").custom_telnet
        self.device = BuiltIn().get_library_instance("CustomKeywords").topology_loader
        self.dut = self.telnet._cache.current.device.name

class TerminalDasan1(TerminalBase):
    """Implementation of Terminal feature for Dasan V5812G"""
    def __init__(self):
        super().__init__()

    def privilege_mode(self):
        command = f"end"
        return self.telnet.send_command(command)
    
    def configure_mode(self):
        command = f"configure terminal"
        return self.telnet.send_command(command)

    def gpon_mode(self):
        command = f"gpon"
        return self.telnet.send_command(command)

    def bridge_mode(self):
        command = f"bridge"
        return self.telnet.send_command(command)

    def interface_gpon_mode(self, link):
        port_alias = self.device.get_port_alias_from_link(self.dut, link)

        
    

class TerminalHuawei1(TerminalBase):
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