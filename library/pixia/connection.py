from robot.api.deco import keyword

class IxiaConnection:
    def __init__(self, base):
        self.base = base

    @keyword
    def connect_to_ixia(self, hostname, session_id):
        """Connects to the Ixia server using the specified hostname and session ID."""
        self.base.start_process()
        self.base.send_line(f"AgtSetServerHostname {hostname}")
        self.base.send_line(f"AgtConnect {session_id}")

    @keyword
    def disconnect_from_ixia(self):
        """Disconnects from the Ixia server."""
        self.base.stop_process()

    @keyword
    def open_new_session(self, session_type):
        """session_type: argument returned by get_session_type.
        it will be used to open a new session.
        It returns the session id of the new session.
        Ex: 73
        """
        return self.base.send_command(f"AgtOpenSession {session_type}")

    @keyword
    def kill_session(self, session_id):
        """Kill the session with the specified session ID."""
        return self.base.send_command(f"AgtCloseSession {session_id}")
