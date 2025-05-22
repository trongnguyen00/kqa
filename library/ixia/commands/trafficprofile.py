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
        
    def add_stream_default(self, port_handle, num_of_streams):
        stream = self.base.send_tcl_command(f"AgtInvoke AddStreamGroups {port_handle} AGT_PACKET_STREAM_GROUP {num_of_streams}")
        return stream
    
    def add_stream_on_profile(self, profile_handle, num_of_streams):
        stream = self.base.send_tcl_command(f"AgtInvoke AgtStreamGroupList AddStreamGroupsWithExistingProfile {profile_handle} AGT_PACKET_STREAM_GROUP {num_of_streams}")
        return stream
    
    def add_stream_and_profile(self, port_handle, num_of_streams):
        """return a list with index 0 is StreamGroupHandle and index 1 is PduHandle"""
        return self.base.send_tcl_command(f"AgtInvoke AgtStreamGroupList AddStreamGroupsWithNewProfile {port_handle} AGT_PACKET_STREAM_GROUP {num_of_streams}")
    
    def remove_stream_ixia(self, stream_group):
        return self.base.send_tcl_command(f"AgtInvoke AgtStreamGroupList Remove {stream_group}")
    
    def get_list_streams(self):
        return self.base.send_tcl_command(f"AgtInvoke AgtStreamGroupList ListHandles")
    
    def set_destination_port(self, stream_group_handle, dest_port):
        """dest port can be a port_handle or a list port_handle"""
        return self.base.send_tcl_command(f"AgtInvoke AgtStreamGroup SetExpectedDestinationPorts {stream_group_handle} {dest_port}")
    
    def add_udp_header(self, stream_group_handle):
        return self.base.send_tcl_command(f"AgtInvoke AgtStreamGroup SetPduHeaders {stream_group_handle} {{ethernet ipv4 udp}}")
    
    def add_udpv6_header(self, stream_group_handle):
        return self.base.send_tcl_command(f"AgtInvoke AgtStreamGroup SetPduHeaders {stream_group_handle} {{ethernet ipv6 udp_v6}}")
    
    def list_header_of_pdu(self, pdu_handle, protocol):
        return self.base.send_tcl_command(f"AgtInvoke AgtPduHeader ListOptionalFields {pdu_handle} {protocol}")
    
    def add_header_to_pdu(self, pdu_handle, protocol, protocol_inst, optional_field):
        return self.base.send_tcl_command(f"AgtInvoke AgtPduHeader EnableOptionalField {pdu_handle} {protocol} {protocol_inst} {optional_field}")
    
    def del_header_of_pdu(self, pdu_handle, protocol, protocol_inst, optional_field):
        return self.base.send_tcl_command(f"AgtInvoke AgtPduHeader DisableOptionalField {pdu_handle} {protocol} {protocol_inst} {optional_field}")

    def set_fix_value_field(self, pdu_handle, protocol, protocol_inst, optional_field, value):
        return self.base.send_tcl_command(f"AgtInvoke AgtPduHeader SetFieldFixedValue {pdu_handle} {protocol} {protocol_inst} {optional_field} {value}")
    
    def get_fix_value_field(self, pdu_handle, protocol, protocol_inst, optional_field):
        return self.base.send_tcl_command(f"AgtInvoke AgtPduHeader GetFieldFixedValue {pdu_handle} {protocol} {protocol_inst} {optional_field}")
    
    def set_incre_value_field(self, pdu_handle, protocol, protocol_inst, optional_field, offset, start_value, num_of_value, step):
        return self.base.send_tcl_command(f"AgtInvoke AgtPduHeader SetFieldIncrementingValueRange {pdu_handle} {protocol} {protocol_inst} {optional_field} {offset} {start_value} {num_of_value} {step}")
    
    def get_incre_value_field(self, pdu_handle, protocol, protocol_inst, optional_field):
        return self.base.send_tcl_command(f"AgtInvoke AgtPduHeader GetFieldIncrementingValueRange {pdu_handle} {protocol} {protocol_inst} {optional_field}")
    
    def set_decre_value_field(self, pdu_handle, protocol, protocol_inst, optional_field, offset, start_value, num_of_value, step):
        return self.base.send_tcl_command(f"AgtInvoke AgtPduHeader SetFieldDecrementingValueRange {pdu_handle} {protocol} {protocol_inst} {optional_field} {offset} {start_value} {num_of_value} {step}")

    def get_decre_value_field(self, pdu_handle, protocol, protocol_inst, optional_field):
        return self.base.send_tcl_command(f"AgtInvoke AgtPduHeader GetFieldDecrementingValueRange {pdu_handle} {protocol} {protocol_inst} {optional_field}")
    
    def set_random_value_field(self, pdu_handle, protocol, protocol_inst, optional_field, offset, min_val, max_val):
        return self.base.send_tcl_command(f"AgtInvoke AgtPduHeader SetFieldRandomValueRange {pdu_handle} {protocol} {protocol_inst} {optional_field} {offset} {min_val} {max_val}")
    
    def get_random_value_field(self, pdu_handle, protocol, protocol_inst, optional_field):
        return self.base.send_tcl_command(f"AgtInvoke AgtPduHeader GetFieldRandomValueRange {pdu_handle} {protocol} {protocol_inst} {optional_field}")
    
    def set_list_value_field(self, pdu_handle, protocol, protocol_inst, optional_field, list_values):
        return self.base.send_tcl_command(f"AgtInvoke AgtPduHeader SetFieldValueList {pdu_handle} {protocol} {protocol_inst} {optional_field} {list_values}")
    
    def get_list_value_field(self, pdu_handle, protocol, protocol_inst, optional_field):
        return self.base.send_tcl_command(f"AgtInvoke AgtPduHeader GetFieldValueList {pdu_handle} {protocol} {protocol_inst} {optional_field}")
    
    def get_all_field_protocol(self, pdu_handle, protocol, protocol_inst):
        return self.base.send_tcl_command(f"AgtInvoke AgtPduHeader ListProtocolFieldsInHeader {pdu_handle} {protocol} {protocol_inst}")
    
    # UDP/TCP modifier
    def set_fix_value_layer4(self, pdu_handle, protocol, protocol_inst, optional_field, value):
        return self.base.send_tcl_command(f"AgtTsuInvoke AgtPduHeader SetFieldFixedValue {pdu_handle} {protocol} {protocol_inst} {optional_field} {value}")
    
    def get_fix_value_layer4(self, pdu_handle, protocol, protocol_inst, optional_field):
        return self.base.send_tcl_command(f"AgtTsuInvoke AgtPduHeader GetFieldFixedValue {pdu_handle} {protocol} {protocol_inst} {optional_field}")
    
    def set_incre_value_layer4(self, pdu_handle, protocol, protocol_inst, optional_field, offset, start_value, num_of_value, step):
        return self.base.send_tcl_command(f"AgtTsuInvoke AgtPduHeader SetFieldIncrementingValueRange {pdu_handle} {protocol} {protocol_inst} {optional_field} {offset} {start_value} {num_of_value} {step}")
    
    def get_incre_value_layer4(self, pdu_handle, protocol, protocol_inst, optional_field):
        return self.base.send_tcl_command(f"AgtTsuInvoke AgtPduHeader GetFieldIncrementingValueRange {pdu_handle} {protocol} {protocol_inst} {optional_field}")
    
    def set_decre_value_layer4(self, pdu_handle, protocol, protocol_inst, optional_field, offset, start_value, num_of_value, step):
        return self.base.send_tcl_command(f"AgtTsuInvoke AgtPduHeader SetFieldDecrementingValueRange {pdu_handle} {protocol} {protocol_inst} {optional_field} {offset} {start_value} {num_of_value} {step}")

    def get_decre_value_layer4(self, pdu_handle, protocol, protocol_inst, optional_field):
        return self.base.send_tcl_command(f"AgtTsuInvoke AgtPduHeader GetFieldDecrementingValueRange {pdu_handle} {protocol} {protocol_inst} {optional_field}")
    
    def set_random_value_layer4(self, pdu_handle, protocol, protocol_inst, optional_field, offset, min_val, max_val):
        return self.base.send_tcl_command(f"AgtTsuInvoke AgtPduHeader SetFieldRandomValueRange {pdu_handle} {protocol} {protocol_inst} {optional_field} {offset} {min_val} {max_val}")
    
    def get_random_value_layer4(self, pdu_handle, protocol, protocol_inst, optional_field):
        return self.base.send_tcl_command(f"AgtTsuInvoke AgtPduHeader GetFieldRandomValueRange {pdu_handle} {protocol} {protocol_inst} {optional_field}")
    
    def set_list_value_layer4(self, pdu_handle, protocol, protocol_inst, optional_field, list_values):
        return self.base.send_tcl_command(f"AgtTsuInvoke AgtPduHeader SetFieldValueList {pdu_handle} {protocol} {protocol_inst} {optional_field} {list_values}")
    
    def get_list_value_layer4(self, pdu_handle, protocol, protocol_inst, optional_field):
        return self.base.send_tcl_command(f"AgtTsuInvoke AgtPduHeader GetFieldValueList {pdu_handle} {protocol} {protocol_inst} {optional_field}")