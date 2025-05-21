from robot.api.deco import keyword
from ixia.commands.trafficprofile import TrafficProfileCommands

class TrafficProfileKeywords:
    def __init__(self, base):
        self.cmd = TrafficProfileCommands(base)

    @keyword
    def create_constant_profile(self, port_handle, profile_type="AGT_CONSTANT_PROFILE"):
        return self.cmd.create_profile(port_handle, profile_type)
    
    @keyword
    def create_burst_profile(self, port_handle, profile_type="AGT_BURST_PROFILE"):
        return self.cmd.create_profile(port_handle, profile_type)

    @keyword
    def create_custom_profile(self, port_handle, profile_type="AGT_CUSTOM_PROFILE"):
        return self.cmd.create_profile(port_handle, profile_type)

    @keyword
    def set_constant_to_burst(self, port_handle, current_type="AgtConstantProfile", new_type="AGT_BURST_PROFILE"):
        return self.cmd.change_mode_profile(port_handle, current_type, new_type)

    @keyword
    def set_constant_to_custom(self, port_handle, current_type="AgtConstantProfile", new_type="AGT_CUSTOM_PROFILE"):
        return self.cmd.change_mode_profile(port_handle, current_type, new_type)

    @keyword
    def set_burst_to_constant(self, port_handle, current_type="AgtBurstProfile", new_type="AGT_CONSTANT_PROFILE"):
        return self.cmd.change_mode_profile(port_handle, current_type, new_type)
    
    @keyword
    def set_burst_to_custom(self, port_handle, current_type="AgtBurstProfile", new_type="AGT_CUSTOM_PROFILE"):
        return self.cmd.change_mode_profile(port_handle, current_type, new_type)

    @keyword
    def set_custom_to_constant(self, port_handle, current_type="AgtCustomProfile", new_type="AGT_CONSTANT_PROFILE"):
        return self.cmd.change_mode_profile(port_handle, current_type, new_type)

    @keyword
    def set_custom_to_burst(self, port_handle, current_type="AgtCustomProfile", new_type="AGT_BURST_PROFILE"):
        return self.cmd.change_mode_profile(port_handle, current_type, new_type)

    @keyword
    def disable_constant_profile(self, profile_handle, current_type="AgtConstantProfile"):
        return self.cmd.disable_profile(profile_handle, current_type)

    @keyword
    def disable_burst_profile(self, profile_handle, current_type="AgtBurstProfile"):
        return self.cmd.disable_profile(profile_handle, current_type)

    @keyword
    def disable_custom_profile(self, profile_handle, current_type="AgtCustomProfile"):
        return self.cmd.disable_profile(profile_handle, current_type)
    
    @keyword
    def enable_constant_profile(self, profile_handle, current_type="AgtConstantProfile"):
        return self.cmd.enable_profile(profile_handle, current_type)
    
    @keyword
    def enable_burst_profile(self, profile_handle, current_type="AgtBurstProfile"):
        return self.cmd.enable_profile(profile_handle, current_type)

    @keyword
    def enable_custom_profile(self, profile_handle, current_type="AgtCustomProfile"):
        return self.cmd.enable_profile(profile_handle, current_type)
    
    @keyword
    def check_is_profile_enable(self, profile_handle, current_type="AgtConstantProfile")
        return self.base.is_profile_enabled(profile_handle, current_type)
    
    @keyword
    def get_list_profile(self, port_handle):
        return self.base.get_list_profile(profile_handle)
    
    @keyword
    def remove_profile_on_port(self, profile_handle):
        return self.base.remove_profile_on_port(profile_handle)
    
    