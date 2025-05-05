from robot.api.deco import keyword

class IxiaPort:
    def __init__(self, base):
        self.base = base

    @keyword
    def port_selector_xfp(self, chassis_id, card_id=1, module_type="AGT_CARD_ONEPORT_10GBASE_R"):
        """Adds a XFP 10G port selector to the session. Returns port_handle."""
        self.base.send_line(f"AgtInvoke AgtPortSelector SetModuleType {chassis_id} {module_type}")
        return self.base.send_command(f"AgtInvoke AgtPortSelector AddPort {chassis_id} {card_id}")

    @keyword
    def port_selector_sfp(self, chassis_id, card_id):
        """Adds a SFP/LAN 1G port selector to the session. Returns port_handle."""
        self.set_port_type(chassis_id, card_id)
        return self.base.send_command(f"AgtInvoke AgtPortSelector AddPort {chassis_id} {card_id}")

    @keyword
    def get_current_port_type(self, chassis_id, card_id):
        """Returns the current type {port_type} of the 1G port."""
        return self.base.send_command(f"AgtInvoke AgtPortSelector GetPortPersonality {chassis_id} {card_id}")

    @keyword
    def get_list_port_types(self, chassis_id, card_id):
        """Returns the list of {port_type} port types for 1G port that can be set for the specified port."""
        return self.base.send_command(f"AgtInvoke AgtPortSelector ListPortPersonalities {chassis_id} {card_id}")

    @keyword
    def set_port_type(self, chassis_id, card_id, port_type="AGT_PERSONALITY_TRI_RATE_ETHERNET_X"):
        """Sets the type of the specified port. Use for 1G port. Default is AGT_PERSONALITY_TRI_RATE_ETHERNET_X = 10/100/1000 Mbps."""
        return self.base.send_command(f"AgtInvoke SetPortPersonality {chassis_id} {card_id} {port_type}")
