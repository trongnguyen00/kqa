# 📁 gpon.py
from robot.api.deco import keyword
from library.terminal.dal.feature_loader import FeatureLoader
import pandas as pd
from library.utils.TableVerificationLibrary import TableVerificationLibrary

class GponKeywords:

    def __init__(self):
        self._gpon = None
        self.table_handler = TableVerificationLibrary()

    @property
    def gpon(self):
        if not self._gpon:
            self._gpon = FeatureLoader("gpon").load()
        return self._gpon

    @keyword
    def get_all_onu_active(self, link):
        return self.gpon.get_all_onu_active(link)
    
    @keyword
    def get_onu_info(self, link, onu_id):
        return self.gpon.get_onu_info(link, onu_id)
    
    @keyword
    def get_current_onu_config(self, link, onu_id):
        return self.gpon.get_current_onu_config(link, onu_id)
    
    @keyword
    def get_onuid_from_serial(self, link, serial):
        all_onu = self.get_all_onu_active(link)
        df = self.table_handler.parse_table(all_onu, '/home/ats/ATS/kqa/library/terminal/dal/template/parse_ont_summary.template')
        match = df[df['SN'] == serial]
        if not match.empty:
            return str(match.iloc[0]['ONT_ID'])
        return None

    @keyword
    def get_onu_version(self, link, onu_id):
        return self.gpon.get_onu_version(link, onu_id)

    @keyword
    def switch_os_onu(self, link, onu_id):
        send_switch_os = self.gpon.switch_os_onu(link, onu_id)
        if "(y/n)" in send_switch_os:
            self.gpon.telnet.send_command("y")
            return "Switch OS command sent successfully, please confirm on the device."

    @keyword
    def get_onu_optical_info(self, link, onu_id):
        return self.gpon.get_onu_optical_info(link, onu_id)

    @keyword
    def get_onu_uni_info(self, link, onu_id, uni_id="all"):
        return self.gpon.get_onu_uni_info(link, onu_id, uni_id)
    
    @keyword
    def set_state_onu_uni_down(self, link, onu_id, uni_id):
        return self.gpon.set_state_onu_uni(link, onu_id, uni_id, "off")
    
    @keyword
    def set_state_onu_uni_up(self, link, onu_id, uni_id):
        return self.gpon.set_state_onu_uni(link, onu_id, uni_id, "on")
    
    @keyword
    def get_onu_iphost_info(self, link, onu_id):
        return self.gpon.get_onu_iphost_info(link, onu_id)