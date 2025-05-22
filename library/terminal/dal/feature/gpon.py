from robot.libraries.BuiltIn import BuiltIn
from library.CustomTelnet import CustomTelnet

class GponDasanBase:
    """Implementation of GPON feature for Dasan base"""
    
    def __init__(self):
        self.telnet = BuiltIn().get_library_instance("CustomTelnet")

class GponDasan1(GponDasanBase):
    """Implementation of GPON feature for Dasan V5816XC"""
    
    def check_onu_active(self, onu_id):
        command = f"show port status {onu_id}"
        return self.telnet.send_command(command)

class GponDasan2(GponDasanBase):
    """Implementation of GPON feature for another Dasan variant"""
    
    def check_onu_active(self, onu_id):
        command = f"show onu info {onu_id}"
        return self.telnet.send_command(command)
