from robot.api.deco import keyword
from ixia.commands.traffictest import TrafficTestCommands

class TrafficTestKeywords:
    def __init__(self, base):
        self.cmd = TrafficTestCommands(base)
        
    @keyword
    def start_traffic(self):
        return self.cmd.start_traffic()
    
    @keyword
    def stop_traffic(self):
        return self.cmd.stop_traffic()
