from robot.libraries.BuiltIn import BuiltIn
from library.CustomTelnet import CustomTelnet

class GponBase:
    """Implementation of GPON feature"""
    
    def __init__(self):
        self.telnet = BuiltIn().get_library_instance("CustomKeywords").custom_telnet
        self.device = BuiltIn().get_library_instance("CustomKeywords").topology_loader
        self.device_info = self.telnet._cache.current.device_info
        self.topology_link = self.telnet._cache.current.topology_link
        self.dut = self.device_info['name']
        

class GponDasan1(GponBase):
    """Implementation of GPON feature for Dasan V5812G"""
    def __init__(self):
        super().__init__()
        
    def get_all_onu_active(self, link):
        port_id = self.device.get_port_index_from_link(self.dut, link)
        command = f"show onu active {port_id}"
        return self.telnet.send_command(command)
    

class GponHuawei1(GponBase):
    """Implementation of GPON feature for MA5800-X7"""
    def __init__(self):
        super().__init__()
    
    def get_all_onu_active(self, link):
        port_id = self.device.get_port_index_from_link(self.dut, link)
        command = f"display ont info summary {port_id}"
        return self.telnet.send_command(command)
    
    def get_onu_info(self, link, onu_id):
        port_id = self.device.get_port_index_from_link(self.dut, link)
        command = f"display ont info {port_id} {onu_id}"
        return self.telnet.send_command(command)
    
    def get_current_onu_config(self, frame_id, slot_id, port_id, onu_id):
        command = f"display current-configuration ont {frame_id}/{slot_id}/{port_id} {onu_id}"
        return self.telnet.send_command(command)
    
    def get_discovered_onu(self, port_id):
        command = f"display ont autofind {port_id}"
        return self.telnet.send_command(command)

    def get_onu_version(self,port_id, onu_id):
        command = f"display ont version {port_id} {onu_id}"
        return self.telnet.send_command(command)

    def switch_os_onu(self, port_id, onu_id):
        command = f"ont rollback software {port_id} {onu_id}"
        self.telnet.write(command)
        time.sleep(0.5)
        output = self.read_very_eager().decode(errors="ignore")
        return output

    def get_onu_optical_info(self, port_id, onu_id):
        command = f"display ont optical-info {port_id} {onu_id}"
        return self.telnet.send_command(command)
    
    def get_onu_uni_info(self, port_id, onu_id, uni_id):
        command = f"display ont port state {port_id} {onu_id} eth-port {uni_id}"
        return self.telnet.send_command(command)

    def set_state_onu_uni(self, port_id, onu_id, uni_id, state):
        command = f"ont port attribute {port_id} {onu_id} eth {uni_id} operational-state {state}"
        return self.telnet.send_command(command)
    
    def get_onu_iphost_info(self, port_id, onu_id):
        command = f"display ont ipconfig {port_id} {onu_id}"
        return self.telnet.send_command(command)