class PortCommands:
    def __init__(self, base):
        self.base = base

    def port_selector_xfp(self, chassis_id, card_id=1, module_type="AGT_CARD_ONEPORT_10GBASE_R"):
        self.base.send_line(f"AgtInvoke AgtPortSelector SetModuleType {chassis_id} {module_type}")
        return self.base.send_tcl_command(f"AgtInvoke AgtPortSelector AddPort {chassis_id} {card_id}")

    def port_selector_sfp(self, chassis_id, card_id):
        self.set_port_type(chassis_id, card_id)
        return self.base.send_tcl_command(f"AgtInvoke AgtPortSelector AddPort {chassis_id} {card_id}")

    def get_current_port_type(self, chassis_id, card_id):
        return self.base.send_tcl_command(f"AgtInvoke AgtPortSelector GetPortPersonality {chassis_id} {card_id}")

    def get_list_port_types(self, chassis_id, card_id):
        return self.base.send_tcl_command(f"AgtInvoke AgtPortSelector ListPortPersonalities {chassis_id} {card_id}")

    def set_port_type(self, chassis_id, card_id, port_type="AGT_PERSONALITY_TRI_RATE_ETHERNET_X"):
        return self.base.send_tcl_command(f"AgtInvoke SetPortPersonality {chassis_id} {card_id} {port_type}")
