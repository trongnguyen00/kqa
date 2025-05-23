# 📁 gpon.py

from robot.api.deco import keyword
from library.terminal.dal.feature_loader import FeatureLoader

class GponKeywords:

    def __init__(self):
        self._gpon = None

    @property
    def gpon(self):
        if not self._gpon:
            self._gpon = FeatureLoader("gpon").load()
        return self._gpon

    @keyword
    def get_all_onu_active(self, port_id):
        return self.gpon.get_all_onu_active(port_id)
    
    @keyword
    def get_onu_info(self, port_id, onu_id):
        return self.gpon.get_onu_info(port_id, onu_id)
    
    @keyword
    def get_current_onu_config(self, frame_id=0, slot_id, port_id, onu_id):
        return self.gpon.get_current_onu_config(frame_id, slot_id, port_id, onu_id)
    
    
