from robot.libraries.BuiltIn import BuiltIn
from library.CustomTelnet import CustomTelnet

class GponBase:
    """Implementation of GPON feature"""
    
    def __init__(self):
        self.telnet = BuiltIn().get_library_instance("CustomKeywords").custom_telnet

class GponDasan1(GponBase):
    """Implementation of GPON feature for Dasan V5812G"""
    
    def get_all_onu_active(self, port_id):
        command = f"show onu active {port_id}"
        return self.telnet.send_command(command)
    

class GponHuawei1(GponBase):
    """Implementation of GPON feature for MA5800-X7"""
    
    def get_all_onu_active(self, port_id):
        command = f"display ont info summary {port_id}"
        return self.telnet.send_command(command)
    
    def get_onu_info(self, port_id, onu_id):
        command = f"display ont info {port_id} {onu_id}"
        return self.telnet.send_command(command)
    
    def get_current_onu_config(self, frame_id, slot_id, port_id, onu_id):
        command = f"display current-configuration ont {frame_id}/{slot_id}/{port_id} {onu_id}"
        return self.telnet.send_command(command)
    
    def get_discovered_onu(self, port_id):
        command = f"display ont autofind {port_id}"
        return self.telnet.send_command(command)
    