from robot.api.deco import keyword

class IxiaSession:
    def __init__(self, base):
        self.base = base

    @keyword
    def get_session_type(self):
        """Returns the session type.
        Ex: RouterTester900
        """
        return self.base.send_command("AgtListSessionTypes")

    @keyword
    def get_session_version(self, session_type):
        return self.base.send_command(f"AgtListSessionVersions {session_type}")

    @keyword
    def get_session_active(self):
        return self.base.send_command("AgtListOpenSessions")

    @keyword
    def set_session_label(self, session_id, label):
        self.base.send_line(f"AgtSetSessionLabel {session_id} {label}")

    @keyword
    def get_session_label(self, session_id):
        return self.base.send_command(f"AgtGetSessionLabel {session_id}")

    @keyword
    def reset_test_session(self):
        return self.base.send_line_and_wait_marker("AgtInvoke AgtTestSession ResetSession")
