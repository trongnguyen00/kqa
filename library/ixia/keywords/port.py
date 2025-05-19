from robot.api.deco import keyword
from ixia.commands.port import PortCommands

class PortKeywords:
    def __init__(self, base):
        self.cmd = PortCommands(base)

    @keyword
    def port_selector_xfp(self, chassis_id, card_id=1, module_type="AGT_CARD_ONEPORT_10GBASE_R"):
        return self.cmd.port_selector_xfp(chassis_id, card_id, module_type)

    @keyword
    def port_selector_sfp(self, chassis_id, card_id):
        return self.cmd.port_selector_sfp(chassis_id, card_id)

    @keyword
    def get_current_port_type(self, chassis_id, card_id):
        return self.cmd.get_current_port_type(chassis_id, card_id)

    @keyword
    def get_list_port_types(self, chassis_id, card_id):
        return self.cmd.get_list_port_types(chassis_id, card_id)

    @keyword
    def set_port_type(self, chassis_id, card_id, port_type="AGT_PERSONALITY_TRI_RATE_ETHERNET_X"):
        return self.cmd.set_port_type(chassis_id, card_id, port_type)
