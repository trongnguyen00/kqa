class SessionCommands:
    def __init__(self, base):
        self.base = base

    def get_type(self):
        return self.base.send_tcl_command("AgtListSessionTypes")

    def get_version(self, session_type):
        return self.base.send_tcl_command(f"AgtListSessionVersions {session_type}")

    def get_active(self):
        return self.base.send_tcl_command("AgtListOpenSessions")

    def set_label(self, session_id, label):
        session_id = int(session_id)
        self.base.send_tcl_command(f"AgtSetSessionLabel {session_id} {label}")

    def get_label(self, session_id):
        return self.base.send_tcl_command(f"AgtGetSessionLabel {session_id}")

    def reset_session(self):
        return self.base.send_line_and_wait_marker("AgtInvoke AgtTestSession ResetSession")
