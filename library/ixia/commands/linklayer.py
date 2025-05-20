class LinkLayerCommands:
    def __init__(self, base):
        self.base = base

    def disable_arp(self, port_handle):
        return self.base.send_tcl_command(f"AgtInvoke AgtArpEmulation Disable {port_handle}")

    def set_ip_tester(self, port_handle, ip_addr, prefix_length, num_addr, step):
        addr_pool = self.get_address_pool(port_handle)
        return self.base.send_tcl_command(f"AgtInvoke AgtEthernetAddressPool SetTesterIpAddresses {addr_pool} {ip_addr} {prefix_length} {num_addr} {step}")

    def set_ip_sut(self, port_handle, new_sut_ip):
        cur_sut_ip = self.base.send_tcl_command(f"AgtInvoke AgtEthernetAddresses ListSutIpAddresses {port_handle}")
        return self.base.send_tcl_command(f"AgtInvoke AgtEthernetAddresses ModifySutIpAddress {port_handle} {cur_sut_ip} {new_sut_ip}")

    def get_address_pool(self, port_handle):
        return self.base.send_tcl_command(f"AgtInvoke AgtEthernetAddresses ListAddressPools {port_handle}")

    def set_mac_tester(self, port_handle, mac_addr, uniq_mac_flag):
        addr_pool = self.get_address_pool(port_handle)
        return self.base.send_tcl_command(f"AgtInvoke AgtEthernetAddressPool SetTesterMacAddresses {addr_pool} {mac_addr}, {uniq_mac_flag}")

    def set_vlan_tags_to_link(self, port_handle):
        addr_pool = self.get_address_pool(port_handle)
        return self.base.send_tcl_command(f"AgtInvoke AgtEthernetAddressPool EnableVlan {addr_pool}")
    
    def set_vlan_id_to_link(self, port_handle, vlan_id):
        addr_pool = self.get_address_pool(port_handle)
        return self.base.send_tcl_command(f"AgtInvoke AgtEthernetAddressPool SetVlanId {addr_pool} {vlan_id}")

    def enable_arp(self, port_handle):
        return self.base.send_tcl_command(f"AgtInvoke AgtArpEmulation Enable {port_handle}")

    def send_arp(self, port_handle):
        return self.base.send_tcl_command(f"AgtInvoke AgtArpEmulation SendAllArpRequests {port_handle}")
