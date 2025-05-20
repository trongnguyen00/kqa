class TrafficProfileCommands:
    def __init__(self, base):
        self.base = base

    def create_profile(self, port_handle, profile_type):
        return self.base.send_tcl_command(f"AgtInvoke AgtProfileList AddProfile {port_handle} {profile_type}")

    def change_mode_profile(self, port_handle, current_type, new_type):
        return self.base.send_tcl_command(f"AgtInvoke {current_type} SetProfileType {port_handle} {new_type}")
    
    def disable_profile(self, profile_handle, current_type):
        return self.base.send_tcl_command(f"AgtInvoke {current_type} Disable {profile_handle}")
    
    def enable_profile(self, profile_handle, current_type):
        return self.base.send_tcl_command(f"AgtInvoke {current_type} Enable {profile_handle}")
    
    def is_profile_enabled(self, profile_handle, current_type):
        return self.base.send_tcl_command(f"AgtInvoke {current_type} IsEnabled {profile_handle}")
    
    def get_list_profile(self, port_handle):
        return self.base.send_tcl_command(f"AgtInvoke AgtProfileList ListProfilesOnPort {profile_handle}")
    
    def remove_profile_on_port(self, profile_handle):
        return self.base.send_tcl_command(f"AgtInvoke AgtProfileList Remove {profile_handle}")
    
    def set_rate_profile(self, current_type, profile_handle, ave_load, unit):
        """
        AGT_UNITS_PACKETS_PER_SEC
         Specifies that the load is given in units of packets/s.
        AGT_UNITS_MBITS_PER_SEC
         Specifies that the load is given in units of Mb/s, expressed as an L2 load.
        AGT_UNITS_PERCENTAGE_LINK_BANDWIDTH
         Specifies that the load is given as a percentage of the link's available bandwidth.
        AGT_UNITS_L3_MBITS_PER_SEC
         Specifies that the load is given in units of Mb/s, expressed as an L3 load. 
        """
        return self.base.send_tcl_command(f"AgtInvoke {current_type} SetAverageLoad {profile_handle} {ave_load} {unit}")
    
    def set_mode_profile(self, current_type, profile_handle, mode):
        """
        Mode have 2 selections:
            AGT_TRAFFIC_PROFILE_MODE_CONTINUOUS
            AGT_TRAFFIC_PROFILE_MODE_ONE_SHOT
        """
        return self.base.send_tcl_command(f"AgtInvoke {current_type} SetMode {profile_handle} {mode}")
        