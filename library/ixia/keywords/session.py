from robot.api.deco import keyword
from ixia.commands.session import SessionCommands

class SessionKeywords:
    def __init__(self, base):
        self.cmd = SessionCommands(base)

    @keyword
    def get_session_type(self):
        return self.cmd.get_type()

    @keyword
    def get_session_version(self, session_type):
        return self.cmd.get_version(session_type)

    @keyword
    def get_session_active(self):
        return self.cmd.get_active()

    @keyword
    def set_session_label(self, session_id, label):
        self.cmd.set_label(session_id, label)

    @keyword
    def get_session_label(self, session_id):
        return self.cmd.get_label(session_id)

    @keyword
    def reset_test_session(self):
        return self.cmd.reset_session()