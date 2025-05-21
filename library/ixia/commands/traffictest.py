class TrafficTestCommands:
    def __init__(self, base):
        self.base = base

    def start_traffic(self):
        return self.base.send_line(f"AgtInvoke AgtTestController StartTest")
    
    def stop_traffic(self):
        return self.base.send_line(f"AgtInvoke AgtTestController StopTest")

    def create_result_dict(self):
        """return a variable: result_var to save result"""
        return self.base.send_tcl_command(f"AgtInvoke AgtStatisticsList Add AGT_STATISTICS")
    
    def add_parameter_measure_result(self, result_var):
        return self.base.send_tcl_command(f"AgtInvoke AgtStatistics SelectStatistics {result_var} {{AGT_STREAM_PACKETS_TRANSMITTED AGT_STREAM_PACKETS_RECEIVED AGT_STREAM_TRANSMIT_THROUGHPUT AGT_STREAM_RECEIVE_THROUGHPUT AGT_STREAM_PACKET_LOSS AGT_STREAM_AVERAGE_LATENCY AGT_STREAM_SEQUENCE_ERRORS}}")
    
    def add_stream_monitored(self, result_var, stream_group_handle):
        return self.base.send_tcl_command(f"AgtInvoke AgtStatistics SelectStreamGroups {result_var} {stream_group_handle}")
    
    def get_results_stats(self, result_var, stream_group_handle, stream_idx, expected_port):
        stats = self.base.send_tcl_command(f"AgtInvoke AgtStatistics GetStreamStatistics {result_var} {stream_group_handle} {stream_idx} {expected_port}")
        return stats