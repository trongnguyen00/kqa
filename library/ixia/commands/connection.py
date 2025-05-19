class ConnectionCommands:
    def __init__(self, base):
        self.base = base

    def connect(self, hostname, session_id):
        self.base.start_process()
        self.base.send_line(f"AgtSetServerHostname {hostname}")
        self.base.send_line(f"AgtConnect {session_id}")

    def disconnect(self):
        self.base.stop_process()

    def open_session(self, session_type):
        return self.base.send_tcl_command(f"AgtOpenSession {session_type}")

    def kill_session(self, session_id):
        return self.base.send_tcl_command(f"AgtCloseSession {session_id}")