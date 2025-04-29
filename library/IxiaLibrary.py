from robot.api.deco import keyword, library
import subprocess
import threading
import time

@library
class IxiaLibrary(object):
    def __init__(self):
        self.process = None
        self.output_lock = threading.Lock()

    @keyword
    def connect_to_ixia(self, server_hostname, session_id):
        """Connects to the Ixia server using the specified hostname and session ID."""
        if self.process is not None:
            raise RuntimeError("Already connected to Tclsh/Ixia.")

        self.process = subprocess.Popen(
            ["tclsh8.6"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            bufsize=0
        )

        self._send_line(f"AgtSetServerHostname {server_hostname}")
        self._send_line(f"AgtConnect {session_id}")

    @keyword
    def send_tcl_command(self, command, timeout=10):
        """Sends a command to the Tclsh process and waits for the output.
        using it when you need to get the output of the command.
        1. command: the command to be sent to tclsh.
        2. timeout: time to wait for the command to finish.
        3. return: the output of the command.
        unless, please using _send_line to send command without get output.
        """
        if self.process is None:
            raise RuntimeError("Tclsh session is not active. Please connect first.")

        with self.output_lock:
            wrapped_command = f"set __robot_output [{command}]\nputs $__robot_output\n"
            self.process.stdin.write(wrapped_command)
            self.process.stdin.flush()

            start_time = time.time()
            while True:
                if time.time() - start_time > timeout:
                    raise TimeoutError("Timeout waiting for command output from tclsh.")
                line = self.process.stdout.readline()
                if line:
                    return line.strip()

    @keyword
    def port_selector_xfp(self, chassis_id, card_id=1, module_type="AGT_CARD_ONEPORT_10GBASE_R"):
        """Adds a XFP 10G port selector to the session.
        Default add with type is 10Gbe LAN XFP.
        Return port_handle
        """
        self._send_line(f"AgtInvoke AgtPortSelector SetModuleType {chassis_id} {module_type}")
        command = f"AgtInvoke AgtPortSelector AddPort {chassis_id} {card_id}"
        return self.send_tcl_command(command)
    
    @keyword
    def get_current_port_type(self, chassis_id, card_id):
        """Returns the current type {port_type} of the 1G port."""
        command = f"AgtInvoke AgtPortSelector GetPortPersonality {chassis_id} {card_id}"
        return self.send_tcl_command(command)
    
    @keyword
    def get_list_port_types(self, chassis_id, card_id):
        """Returns the list of {port_type} port types for 1G port that can be set for the specified port."""
        command = f"AgtInvoke AgtPortSelector ListPortPersonalities {chassis_id} {card_id}"
        return self.send_tcl_command(command)

    @keyword
    def set_port_type(self, chassis_id, card_id, port_type="AGT_PERSONALITY_TRI_RATE_ETHERNET_X"):
        """Sets the type of the specified port. Use for 1G port"""
        command = f"AgtInvoke SetPortPersonality {chassis_id} {card_id} {port_type}"
        return self.send_tcl_command(command)

    @keyword
    def port_selector_sfp(self, chassis_id, card_id):
        """Adds a SFP/LAN 1G port selector to the session.
        Using for 1Gbe SFP/LAN.
        Return port_handle
        """
        self.set_port_type(chassis_id, card_id)
        command = f"AgtInvoke AgtPortSelector AddPort {chassis_id} {card_id}"
        return self.send_tcl_command(command)

    @keyword
    def get_list_media_type(self, port_handle):
        """Returns the list of {media_type} media types for 1G port that can be set for the specified port."""
        command = f"AgtInvoke AgtPhysicalInterface ListAvailableMediaTypes {port_handle}"
        return self.send_tcl_command(command)

    @keyword
    def set_media_type(self, port_handle, media_type):
        """Sets the media type for the specified port."""
        command = f"AgtInvoke AgtPhysicalInterface SetMediaType {port_handle} {media_type}"
        return self.send_tcl_command(command)

    @keyword
    def get_list_modules(self):
        """Returns the list numbers of all modules in the chassis.
        Ex: 101 102 104 201 202 203 204
        """
        command = f"AgtInvoke AgtPortSelector ListModules"
        return self.send_tcl_command(command)

    @keyword
    def list_module_types(self, module_number):
        """Returns the type of the specified module."""
        command = f"AgtInvoke AgtPortSelector ListModuleTypes {module_number}"
        return self.send_tcl_command(command)

    @keyword
    def set_module_types(self, module_number, module_type):
        """Sets the type of the specified module."""
        command = f"AgtSetModuAgtInvoke AgtPortSelector SetModuleTypeleType {module_number} {module_type}"
        return self.send_tcl_command(command)

    @keyword
    def get_session_type(self):
        """Returns the session type.
        Ex: RouterTester900
        """
        command = f"AgtListSessionTypes"
        return self.send_tcl_command(command)

    @keyword
    def get_session_version(self, session_type):
        """Returns the current version of the session type.
        Ex: {7.60 GA SP2 Release}
        """
        command = f"AgtListSessionVersions {session_version}"
        return self.send_tcl_command(command)

    @keyword
    def get_session_active(self):
        """Returns the all session ID that are actived.
        The value retuns a list of session ID.
        Ex: 46 60 62 66 67 68 73
        """
        command = f"AgtListOpenSessions"
        return self.send_tcl_command(command)

    @keyword
    def set_session_label(self, session_id, label):
        """Sets the label for the specified session."""
        command = f"AgtSetSessionLabel {session_id} {label}"
        return self._send_line(command)

    @keyword
    def get_session_label(self, session_id):
        """Gets the label for the specified session."""
        command = f"AgtGetSessionLabel {session_id}"
        return self.send_tcl_command(command)

    @keyword
    def disconnect_from_ixia(self):
        if self.process is not None:
            with self.output_lock:
                self.process.stdin.write("exit\n")
                self.process.stdin.flush()
                self.process.wait(timeout=5)
                self.process = None

    @keyword
    def kill_session(self, session_id):
        """Kill the session with the specified session ID."""
        command = f"AgtCloseSession {session_id}"
        return self.send_tcl_command(command)

    @keyword
    def open_new_session(self, session_type):
        """session_type: argument returned by get_session_type.
        it will be used to open a new session.
        It returns the session id of the new session.
        Ex: 73
        """
        command = f"AgtOpenSession {session_type}"
        return self.send_tcl_command(command)

    @keyword
    def reset_test_session(self):
        """Reset the test session.
        Waiting for the session to be reset."""
        command = f"AgtInvoke AgtTestSession ResetSession"
        return self._send_line_and_wait_success(command)

    # Helper
    def _send_line(self, line):
        """Helper to send command without get output."""
        self.process.stdin.write(line + "\n")
        self.process.stdin.flush()
        self.process.stdout.readline()


    def _send_line_and_wait_success(self, line, marker="<<<READY>>>", timeout=100, poll_interval=5):
        self.process.stdin.write(line + "\n")
        self.process.stdin.write(f'puts "{marker}"\n')
        self.process.stdin.flush()

        output_lines = []
        start_time = time.time()

        while True:
            if time.time() - start_time > timeout:
                raise TimeoutError(f"Timeout waiting for TCL to complete command: {line}")

            line_out = self.process.stdout.readline()
            if not line_out:
                continue

            line_out = line_out.strip()
            output_lines.append(line_out)

            if marker in line_out:
                break

            time.sleep(poll_interval)

        return "\n".join(output_lines)

