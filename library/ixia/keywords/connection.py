from robot.api.deco import keyword
from library.ixia.commands.connection import ConnectionCommands

class ConnectionKeywords:
    def __init__(self, base):
        self.cmd = ConnectionCommands(base)

    @keyword
    def connect_to_ixia(self, hostname, session_id):
        self.cmd.connect(hostname, session_id)

    @keyword
    def disconnect_from_ixia(self):
        self.cmd.disconnect()

    @keyword
    def open_new_session(self, session_type):
        return self.cmd.open_session(session_type)

    @keyword
    def kill_session(self, session_id):
        return self.cmd.kill_session(session_id)