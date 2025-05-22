# 📁 gpon.py

from robot.api.deco import keyword
from library.terminal.dal.feature_loader import FeatureLoader

class GponKeywords:

    def __init__(self):
        self._gpon = None  # trì hoãn khởi tạo

    @property
    def gpon(self):
        if not self._gpon:
            self._gpon = FeatureLoader("gpon").load()
        return self._gpon

    @keyword
    def check_onu_active(self, onu_id):
        return self.gpon.check_onu_active(onu_id)
