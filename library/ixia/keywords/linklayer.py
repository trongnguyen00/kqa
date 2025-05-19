from robot.api.deco import keyword
from ixia.commands.linklayer import LinkLayerCommands

class LinkLayerKeywords:
    def __init__(self, base):
        self.cmd = LinkLayerCommands(base)

    @keyword
    def disable_arp(self, port_handle):
        return self.cmd.disable_arp(port_handle)

    def set_ip_tester(self, port_handle, ip_addr, prefix_length=24, num_addr=1, step=1):
        return self.cmd.set_ip_tester(port_handle, ip_addr, prefix_length, num_addr, step)
    
    def set_ip_sut(seft, port_handle, new_sut_ip):
        return self.cmd.set_ip_sut(port_handle, new_sut_ip)

    def set_mac_tester(self, port_handle, mac_addr, uniq_mac_flag=1):
        return self.cmd.set_mac_tester(port_handle, mac_addr, uniq_mac_flag)

    def set_vlan_tags_to_link(self, port_handle):
        return self.cmd.set_vlan_tags_to_link(port_handle)

    def set_vlan_id_to_link(self, port_handle, vlan_id):
        return self.cmd.set_vlan_id_to_link(port_handle, vlan_id)

    def enable_arp(self, port_handle):
        return self.cmd.enable_arp(port_handle)

    def send_arp(self, port_handle):
        return self.cmd.send_arp(port_handle)