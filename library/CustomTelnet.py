#  Copyright 2008-2015 Nokia Networks
#  Copyright 2016-     Robot Framework Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import inspect
import re
import socket
import struct
import telnetlib
import time
from contextlib import contextmanager
import yaml

try:
    import pyte
except ImportError:
    pyte = None

from robot.api import logger
from robot.api.deco import keyword, library
from robot.libraries.BuiltIn import BuiltIn
from robot.utils import (
    ConnectionCache, is_truthy, secs_to_timestr, seq2str, timestr_to_secs
)
from robot.version import get_version

@library(scope='GLOBAL')
class CustomTelnet(telnetlib.Telnet):
    """A library providing communication over Telnet connections with enhanced features.
    
    This library combines the functionality of Telnet connection management,
    command execution, and command group handling into a single class.
    """
    
    NEW_ENVIRON_IS = b"\x00"
    NEW_ENVIRON_VAR = b"\x00"
    NEW_ENVIRON_VALUE = b"\x01"
    INTERNAL_UPDATE_FREQUENCY = 0.03
    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LIBRARY_VERSION = get_version()

    def __init__(
        self,
        timeout="3 seconds",
        newline="CRLF",
        prompt=None,
        prompt_is_regexp=False,
        encoding="UTF-8",
        encoding_errors="ignore",
        default_log_level="INFO",
        window_size=None,
        environ_user=None,
        terminal_emulation=False,
        terminal_type=None,
        telnetlib_log_level="TRACE",
        connection_timeout=None,
    ):
        """Initialize with optional configuration parameters."""
        super().__init__()
        self._timeout = timestr_to_secs(timeout)
        self._connection_timeout = timestr_to_secs(connection_timeout) if connection_timeout else None
        self._newline = newline.replace("LF", "\n").replace("CR", "\r")
        self._prompt = (prompt, prompt_is_regexp)
        self._encoding = (encoding.upper(), encoding_errors)
        self._default_log_level = default_log_level
        self._window_size = window_size
        self._environ_user = self._encode(environ_user) if environ_user else None
        self._terminal_emulation = terminal_emulation
        self._terminal_type = self._encode(terminal_type) if terminal_type else None
        self._telnetlib_log_level = telnetlib_log_level
        self._cache = ConnectionCache()
        self._conn = None
        self._terminal_emulator = self._check_terminal_emulation(terminal_emulation)
        self._opt_responses = []
        self.current_prompt_level = 0

    def get_keyword_names(self):
        """Return list of all available keywords."""
        return self._get_library_keywords() + self._get_connection_keywords()

    def _get_library_keywords(self):
        """Get keywords from this library."""
        return [name for name in dir(self) if self._is_keyword(name, self, ["get_keyword_names"])]

    def _get_connection_keywords(self):
        """Get keywords from telnetlib.Telnet."""
        excluded = [name for name in dir(telnetlib.Telnet()) 
                   if name not in ["write", "read", "read_until"]]
        return [name for name in dir(telnetlib.Telnet()) 
                if self._is_keyword(name, telnetlib.Telnet(), excluded)]

    def _is_keyword(self, name, source, excluded):
        """Check if a method should be exposed as a keyword."""
        return (name not in excluded
                and not name.startswith("_")
                and name != "get_keyword_names"
                and inspect.ismethod(getattr(source, name)))

    @keyword
    def open_connection(
        self,
        host,
        alias=None,
        port=23,
        timeout=None,
        newline=None,
        prompt=None,
        prompt_is_regexp=False,
        encoding=None,
        encoding_errors=None,
        default_log_level=None,
        window_size=None,
        environ_user=None,
        terminal_emulation=None,
        terminal_type=None,
        telnetlib_log_level=None,
        connection_timeout=None,
    ):
        """Opens a new Telnet connection to the given host and port."""
        if self.sock:
            self.close()
            
        if connection_timeout is None:
            super().__init__(host, int(port) if port else 23)
        else:
            super().__init__(host, int(port) if port else 23, connection_timeout)
            
        self._set_timeout(timeout or self._timeout)
        self._set_newline(newline or self._newline)
        self._set_prompt(prompt or self._prompt[0], prompt_is_regexp)
        self._set_encoding(encoding or self._encoding[0], encoding_errors or self._encoding[1])
        self._set_default_log_level(default_log_level or self._default_log_level)
        self._window_size = window_size or self._window_size
        self._environ_user = self._encode(environ_user) if environ_user else self._environ_user
        if terminal_emulation is not None:
            self._terminal_emulator = self._check_terminal_emulation(terminal_emulation)
        self._terminal_type = self._encode(terminal_type) if terminal_type else self._terminal_type
        self._set_telnetlib_log_level(telnetlib_log_level or self._telnetlib_log_level)
        
        return self._cache.register(self, alias)

    @keyword
    def switch_connection(self, index_or_alias):
        """Switches between active connections using an index or an alias."""
        old_index = self._cache.current_index
        self._conn = self._cache.switch(index_or_alias)
        return old_index

    @keyword
    def close_all_connections(self):
        """Closes all open connections and empties the connection cache."""
        self._conn = self._cache.close_all()

    @keyword
    def connect_to_dut(self, device_name):
        """Connect to DUT using topology data from TopologyLoader."""
        topo = BuiltIn().get_library_instance("CustomKeywords").topology_loader
        device = topo.get_device(device_name)
        topology_link = topo.get_topology_links(device_name)
        conn = device.connections

        ip = conn.get("ip")
        port = conn.get("port", 23)
        username = conn.get("username")
        password = conn.get("password")
        api = device.api

        login_info = self._get_login_prompt_by_api(api)
        login_prompt = login_info["login_prompt"]
        password_prompt = login_info["password_prompt"]

        self.open_connection(ip, port=port, prompt=None, prompt_is_regexp=False)
        output = self.login(
            username=username,
            password=password,
            login_prompt=login_prompt,
            password_prompt=password_prompt
        )

        self.write("")
        prompt_output = ""
        for _ in range(10):
            time.sleep(0.5)
            chunk = self.read_very_eager().decode(errors="ignore")
            if chunk:
                prompt_output += chunk
                break

        lines = prompt_output.strip().splitlines()
        if not lines:
            raise AssertionError("No prompt detected after sending ENTER.")

        exact_prompt = lines[-1].strip()
        self._set_prompt(exact_prompt, prompt_is_regexp=False)
        output += prompt_output

        self._cache.current.device_info = {
            "name": device.name,
            "api": device.api,
            "model": device.model,
            "connections": device.connections,
            "custom": device.custom
        }
        self._cache.current.topology_link = topology_link
        # self._cache.current.dut = device_name

        return output

    @keyword
    def send_command(self, command, reset_prompt=False):
        """Send command and optionally reset prompt."""
        self.write(command)
        if reset_prompt:
            self.write("")
            time.sleep(0.5)
            output = self.read_very_eager().decode(errors="ignore")
            lines = output.strip().splitlines()
            if not lines:
                raise AssertionError("Không phát hiện được prompt sau khi gửi ENTER.")
            last_line = lines[-1]
            prompt_candidate = last_line.strip()
            self._set_prompt(prompt_candidate, prompt_is_regexp=False)
            return prompt_candidate
        else:
            return self.read_until_prompt()

    @keyword
    def send_commands_from_group(self, file_path, command_group, **variables):
        """Send commands from a YAML group file."""
        with open(file_path, 'r') as file:
            yaml_data = yaml.safe_load(file)

        commands = yaml_data['commands'][command_group][0]['shell'].splitlines()
        commands = self._replace_variables(commands, variables)

        for line in commands:
            line = line.strip()
            if not line or line == '!':
                self._adjust_prompt_level(0)
                continue

            level = self._get_indent_level(line)
            command = line.lstrip()

            self._adjust_prompt_level(level)
            self._execute(command)

        self._adjust_prompt_level(0)

    @keyword
    def set_timeout(self, timeout):
        """Sets the timeout used for waiting output in the current connection."""
        self._verify_connection()
        old = self._timeout
        self._set_timeout(timeout)
        return secs_to_timestr(old)

    @keyword
    def set_newline(self, newline):
        """Sets the newline used by `Write` keyword in the current connection."""
        self._verify_connection()
        if self._terminal_emulator:
            raise AssertionError("Newline can not be changed when terminal emulation is used.")
        old = self._newline
        self._set_newline(newline)
        return old

    @keyword
    def set_prompt(self, prompt, prompt_is_regexp=False):
        """Sets the prompt used by `Read Until Prompt` and `Login` in the current connection."""
        self._verify_connection()
        old = self._prompt
        self._set_prompt(prompt, prompt_is_regexp)
        if old[1]:
            return old[0].pattern, True
        return old

    @keyword
    def set_encoding(self, encoding=None, errors=None):
        """Sets the encoding to use for writing and reading in the current connection."""
        self._verify_connection()
        if self._terminal_emulator:
            raise AssertionError("Encoding can not be changed when terminal emulation is used.")
        old = self._encoding
        self._set_encoding(encoding or old[0], errors or old[1])
        return old

    @keyword
    def set_telnetlib_log_level(self, level):
        """Sets the log level used for logging in the underlying telnetlib."""
        self._verify_connection()
        old = self._telnetlib_log_level
        self._set_telnetlib_log_level(level)
        return old

    @keyword
    def set_default_log_level(self, level):
        """Sets the default log level used for logging in the current connection."""
        self._verify_connection()
        old = self._default_log_level
        self._set_default_log_level(level)
        return old

    @keyword
    def close_connection(self, loglevel=None):
        """Closes the current Telnet connection."""
        if self.sock:
            self.sock.shutdown(socket.SHUT_RDWR)
        self.close()
        output = self._decode(self.read_all())
        self._log(output, loglevel)
        return output

    @keyword
    def login(
        self,
        username,
        password,
        login_prompt="login: ",
        password_prompt="Password: ",
        login_timeout="1 second",
        login_incorrect="Login incorrect",
    ):
        """Logs in to the Telnet server with the given user information."""
        output = self._submit_credentials(username, password, login_prompt, password_prompt)
        if self._prompt_is_set():
            success, output2 = self._read_until_prompt()
        else:
            success, output2 = self._verify_login_without_prompt(login_timeout, login_incorrect)
        output += output2
        self._log(output)
        if not success:
            raise AssertionError("Login incorrect")
        return output

    @keyword
    def write(self, text, loglevel=None):
        """Writes the given text plus a newline into the connection."""
        newline = self._get_newline_for(text)
        if newline in text:
            raise RuntimeError(
                "'Write' keyword cannot be used with strings "
                "containing newlines. Use 'Write Bare' instead."
            )
        self.write_bare(text + newline)
        return self.read_until(self._newline, loglevel)

    @keyword
    def write_bare(self, text):
        """Writes the given text, and nothing else, into the connection."""
        self._verify_connection()
        super().write(self._encode(text))

    @keyword
    def write_until_expected_output(
        self,
        text,
        expected,
        timeout,
        retry_interval,
        loglevel=None,
    ):
        """Writes the given text repeatedly, until expected appears in the output."""
        timeout = timestr_to_secs(timeout)
        retry_interval = timestr_to_secs(retry_interval)
        maxtime = time.time() + timeout
        while time.time() < maxtime:
            self.write_bare(text)
            self.read_until(text, loglevel)
            try:
                with self._custom_timeout(retry_interval):
                    return self.read_until(expected, loglevel)
            except AssertionError:
                pass
        raise NoMatchError(expected, timeout)

    @keyword
    def write_control_character(self, character):
        """Writes the given control character into the connection."""
        self._verify_connection()
        self.sock.sendall(telnetlib.IAC + self._get_control_character(character))

    @keyword
    def read(self, loglevel=None):
        """Reads everything that is currently available in the output."""
        self._verify_connection()
        output = self._decode(self.read_very_eager())
        if self._terminal_emulator:
            self._terminal_emulator.feed(output)
            output = self._terminal_emulator.read()
        self._log(output, loglevel)
        return output

    @keyword
    def read_until(self, expected, loglevel=None):
        """Reads output until expected text is encountered."""
        success, output = self._read_until(expected)
        self._log(output, loglevel)
        if not success:
            raise NoMatchError(expected, self._timeout, output)
        return output

    @keyword
    def read_until_regexp(self, *expected):
        """Reads output until any of the expected regular expressions match."""
        if not expected:
            raise RuntimeError("At least one pattern required")
        if self._is_valid_log_level(expected[-1]):
            loglevel = expected[-1]
            expected = expected[:-1]
        else:
            loglevel = None
        success, output = self._read_until_regexp(*expected)
        self._log(output, loglevel)
        if not success:
            expected = [e if isinstance(e, str) else e.pattern for e in expected]
            raise NoMatchError(expected, self._timeout, output)
        return output

    @keyword
    def read_until_prompt(self, loglevel=None, strip_prompt=False):
        """Reads output until the prompt is encountered."""
        if not self._prompt_is_set():
            raise RuntimeError("Prompt is not set.")
        success, output = self._read_until_prompt()
        self._log(output, loglevel)
        if not success:
            prompt, regexp = self._prompt
            pattern = prompt.pattern if regexp else prompt
            raise AssertionError(
                f"Prompt '{pattern}' not found in {secs_to_timestr(self._timeout)}."
            )
        if strip_prompt:
            output = self._strip_prompt(output)
        return output

    @keyword
    def execute_command(self, command, loglevel=None, strip_prompt=False):
        """Executes the given command and reads, logs, and returns everything until the prompt."""
        self.write(command, loglevel)
        return self.read_until_prompt(loglevel, strip_prompt)

    @keyword
    def get_current_prompt(self):
        """Return current prompt"""
        prompt, is_regexp = self._prompt
        return prompt.pattern if is_regexp else prompt

    @keyword
    def list_all_connections(self):
        """Return a list of connection alias"""
        return self._cache._connections.keys()

    # Helper methods
    def _replace_variables(self, commands, variables):
        """Replace variables in commands."""
        result = []
        for cmd in commands:
            for key, value in variables.items():
                cmd = cmd.replace(f"{{{{{key}}}}}", str(value))
            result.append(cmd)
        return result

    def _get_indent_level(self, line):
        """Get indentation level of a line."""
        return len(line) - len(line.lstrip())

    def _adjust_prompt_level(self, target):
        """Adjust prompt level by sending exit commands."""
        while self.current_prompt_level > target:
            self.write("exit")
            self.read_until_regexp(r"(#|>)")
            self.current_prompt_level -= 1
        while self.current_prompt_level < target:
            self.read_until_regexp(r"(#|>)")
            self.current_prompt_level += 1

    def _execute(self, command):
        """Execute a command and verify output."""
        self.write(command)
        output = self.read_until_regexp(r"(#|>)")
        if "% Invalid input" in output or "Error" in output:
            raise RuntimeError(f"Lỗi khi gửi lệnh: {command}\nOutput: {output}")

    def _get_login_prompt_by_api(self, api):
        """Get login prompts based on API type."""
        mapping = {
            "ISAM_7360": {
                "login_prompt": "login: ",
                "password_prompt": "password: "
            },
            "MA5800": {
                "login_prompt": ">>User name:",
                "password_prompt": ">>User password:"
            }
        }
        return mapping.get(api, {
            "login_prompt": "login: ",
            "password_prompt": "Password: "
        })

    def _set_timeout(self, timeout):
        self._timeout = timestr_to_secs(timeout)

    def _set_newline(self, newline):
        self._newline = newline.replace("LF", "\n").replace("CR", "\r")

    def _set_prompt(self, prompt, prompt_is_regexp):
        if prompt_is_regexp:
            self._prompt = (re.compile(prompt), True)
        else:
            self._prompt = (prompt, False)

    def _set_encoding(self, encoding, errors):
        self._encoding = (encoding.upper(), errors)

    def _set_default_log_level(self, level):
        if level is None or not self._is_valid_log_level(level):
            raise AssertionError(f"Invalid log level '{level}'")
        self._default_log_level = level.upper()

    def _set_telnetlib_log_level(self, level):
        if level.upper() == "NONE":
            self._telnetlib_log_level = "NONE"
        elif self._is_valid_log_level(level) is False:
            raise AssertionError(f"Invalid log level '{level}'")
        self._telnetlib_log_level = level.upper()

    def _is_valid_log_level(self, level):
        if level is None:
            return True
        if not isinstance(level, str):
            return False
        return level.upper() in ("TRACE", "DEBUG", "INFO", "WARN")

    def _encode(self, text):
        if isinstance(text, (bytes, bytearray)):
            return text
        if self._encoding[0] == "NONE":
            return text.encode("ASCII")
        return text.encode(*self._encoding)

    def _decode(self, bytes):
        if self._encoding[0] == "NONE":
            return bytes
        return bytes.decode(*self._encoding)

    def _verify_connection(self):
        if not self.sock:
            raise RuntimeError("No connection open")

    def _log(self, msg, level=None):
        msg = msg.strip()
        if msg:
            logger.write(msg, level or self._default_log_level)

    def _check_terminal_emulation(self, terminal_emulation):
        if not terminal_emulation:
            return False
        if not pyte:
            raise RuntimeError(
                "Terminal emulation requires pyte module!\n"
                "http://pypi.python.org/pypi/pyte/"
            )
        return TerminalEmulator(window_size=self._window_size, newline=self._newline)

    def _prompt_is_set(self):
        return self._prompt[0] is not None

    def _get_newline_for(self, text):
        if isinstance(text, (bytes, bytearray)):
            return self._encode(self._newline)
        return self._newline

    def _submit_credentials(self, username, password, login_prompt, password_prompt):
        output = self.read_until(login_prompt, "TRACE")
        self.write_bare(username + self._newline)
        output += self.read_until(password_prompt, "TRACE")
        self.write_bare(password + self._newline)
        return output

    def _verify_login_without_prompt(self, delay, incorrect):
        time.sleep(timestr_to_secs(delay))
        output = self.read("TRACE")
        success = incorrect not in output
        return success, output

    def _read_until(self, expected):
        self._verify_connection()
        if self._terminal_emulator:
            return self._terminal_read_until(expected)
        expected = self._encode(expected)
        output = super().read_until(expected, self._timeout)
        return output.endswith(expected), self._decode(output)

    def _read_until_regexp(self, *expected):
        self._verify_connection()
        if self._terminal_emulator:
            return self._terminal_read_until_regexp(expected)
        expected = [self._encode(e) if isinstance(e, str) else e for e in expected]
        return self._telnet_read_until_regexp(expected)

    def _read_until_prompt(self):
        prompt, regexp = self._prompt
        read_until = self._read_until_regexp if regexp else self._read_until
        return read_until(prompt)

    def _strip_prompt(self, output):
        prompt, regexp = self._prompt
        if not regexp:
            length = len(prompt)
        else:
            match = prompt.search(output)
            length = match.end() - match.start()
        return output[:-length]

    @contextmanager
    def _custom_timeout(self, timeout):
        old = self.set_timeout(timeout)
        try:
            yield
        finally:
            self.set_timeout(old)

    def _get_control_character(self, int_or_name):
        try:
            ordinal = int(int_or_name)
            return bytes(bytearray([ordinal]))
        except ValueError:
            return self._convert_control_code_name_to_character(int_or_name)

    def _convert_control_code_name_to_character(self, name):
        code_names = {
            "BRK": telnetlib.BRK,
            "IP": telnetlib.IP,
            "AO": telnetlib.AO,
            "AYT": telnetlib.AYT,
            "EC": telnetlib.EC,
            "EL": telnetlib.EL,
            "NOP": telnetlib.NOP,
        }
        try:
            return code_names[name]
        except KeyError:
            raise RuntimeError(f"Unsupported control character '{name}'.")

    def _negotiate_options(self, sock, cmd, opt):
        if cmd in (telnetlib.DO, telnetlib.DONT, telnetlib.WILL, telnetlib.WONT):
            if (cmd, opt) in self._opt_responses:
                return
            self._opt_responses.append((cmd, opt))

        if opt == telnetlib.ECHO and cmd in (telnetlib.WILL, telnetlib.WONT):
            self._opt_echo_on(opt)
        elif cmd == telnetlib.DO and opt == telnetlib.TTYPE and self._terminal_type:
            self._opt_terminal_type(opt, self._terminal_type)
        elif cmd == telnetlib.DO and opt == telnetlib.NEW_ENVIRON and self._environ_user:
            self._opt_environ_user(opt, self._environ_user)
        elif cmd == telnetlib.DO and opt == telnetlib.NAWS and self._window_size:
            self._opt_window_size(opt, *self._window_size)
        elif opt != telnetlib.NOOPT:
            self._opt_dont_and_wont(cmd, opt)

    def _opt_echo_on(self, opt):
        return self.sock.sendall(telnetlib.IAC + telnetlib.DO + opt)

    def _opt_terminal_type(self, opt, terminal_type):
        self.sock.sendall(telnetlib.IAC + telnetlib.WILL + opt)
        self.sock.sendall(
            telnetlib.IAC
            + telnetlib.SB
            + telnetlib.TTYPE
            + self.NEW_ENVIRON_IS
            + terminal_type
            + telnetlib.IAC
            + telnetlib.SE
        )

    def _opt_environ_user(self, opt, environ_user):
        self.sock.sendall(telnetlib.IAC + telnetlib.WILL + opt)
        self.sock.sendall(
            telnetlib.IAC
            + telnetlib.SB
            + telnetlib.NEW_ENVIRON
            + self.NEW_ENVIRON_IS
            + self.NEW_ENVIRON_VAR
            + b"USER"
            + self.NEW_ENVIRON_VALUE
            + environ_user
            + telnetlib.IAC
            + telnetlib.SE
        )

    def _opt_window_size(self, opt, window_x, window_y):
        self.sock.sendall(telnetlib.IAC + telnetlib.WILL + opt)
        self.sock.sendall(
            telnetlib.IAC
            + telnetlib.SB
            + telnetlib.NAWS
            + struct.pack("!HH", window_x, window_y)
            + telnetlib.IAC
            + telnetlib.SE
        )

    def _opt_dont_and_wont(self, cmd, opt):
        if cmd in (telnetlib.DO, telnetlib.DONT):
            self.sock.sendall(telnetlib.IAC + telnetlib.WONT + opt)
        elif cmd in (telnetlib.WILL, telnetlib.WONT):
            self.sock.sendall(telnetlib.IAC + telnetlib.DONT + opt)

    def msg(self, msg, *args):
        if self._telnetlib_log_level != "NONE":
            logger.write(msg % args, self._telnetlib_log_level)

    @property
    def _terminal_frequency(self):
        return min(self.INTERNAL_UPDATE_FREQUENCY, self._timeout)

    def _terminal_read_until(self, expected):
        max_time = time.time() + self._timeout
        output = self._terminal_emulator.read_until(expected)
        if output:
            return True, output
        while time.time() < max_time:
            output = super().read_until(
                self._encode(expected), self._terminal_frequency
            )
            self._terminal_emulator.feed(self._decode(output))
            output = self._terminal_emulator.read_until(expected)
            if output:
                return True, output
        return False, self._terminal_emulator.read()

    def _terminal_read_until_regexp(self, expected_list):
        max_time = time.time() + self._timeout
        regexps_bytes = [self._to_byte_regexp(rgx) for rgx in expected_list]
        regexps_unicode = [
            re.compile(self._decode(rgx.pattern)) for rgx in regexps_bytes
        ]
        out = self._terminal_emulator.read_until_regexp(regexps_unicode)
        if out:
            return True, out
        while time.time() < max_time:
            output = self.expect(regexps_bytes, self._terminal_frequency)[-1]
            self._terminal_emulator.feed(self._decode(output))
            out = self._terminal_emulator.read_until_regexp(regexps_unicode)
            if out:
                return True, out
        return False, self._terminal_emulator.read()

    def _telnet_read_until_regexp(self, expected_list):
        expected = [self._to_byte_regexp(exp) for exp in expected_list]
        try:
            index, _, output = self.expect(expected, self._timeout)
        except TypeError:
            index, output = -1, b""
        return index != -1, self._decode(output)

    def _to_byte_regexp(self, exp):
        if isinstance(exp, (bytes, bytearray)):
            return re.compile(exp)
        if isinstance(exp, str):
            return re.compile(self._encode(exp))
        pattern = exp.pattern
        if isinstance(pattern, (bytes, bytearray)):
            return exp
        return re.compile(self._encode(pattern))


class TerminalEmulator:
    def __init__(self, window_size=None, newline="\r\n"):
        self._rows, self._columns = window_size or (200, 200)
        self._newline = newline
        self._stream = pyte.Stream()
        self._screen = pyte.HistoryScreen(self._rows, self._columns, history=100000)
        self._stream.attach(self._screen)
        self._buffer = ""
        self._whitespace_after_last_feed = ""

    @property
    def current_output(self):
        return self._buffer + self._dump_screen()

    def _dump_screen(self):
        return (
            self._get_history(self._screen)
            + self._get_screen(self._screen)
            + self._whitespace_after_last_feed
        )

    def _get_history(self, screen):
        if not screen.history.top:
            return ""
        rows = []
        for row in screen.history.top:
            data = (char.data for _, char in sorted(row.items()))
            rows.append("".join(data).rstrip())
        return self._newline.join(rows).rstrip(self._newline) + self._newline

    def _get_screen(self, screen):
        rows = (row.rstrip() for row in screen.display)
        return self._newline.join(rows).rstrip(self._newline)

    def feed(self, text):
        self._stream.feed(text)
        self._whitespace_after_last_feed = text[len(text.rstrip()) :]

    def read(self):
        current_out = self.current_output
        self._update_buffer("")
        return current_out

    def read_until(self, expected):
        current_out = self.current_output
        exp_index = current_out.find(expected)
        if exp_index != -1:
            self._update_buffer(current_out[exp_index + len(expected) :])
            return current_out[: exp_index + len(expected)]
        return None

    def read_until_regexp(self, regexp_list):
        current_out = self.current_output
        for rgx in regexp_list:
            match = rgx.search(current_out)
            if match:
                self._update_buffer(current_out[match.end() :])
                return current_out[: match.end()]
        return None

    def _update_buffer(self, terminal_buffer):
        self._buffer = terminal_buffer
        self._whitespace_after_last_feed = ""
        self._screen.reset()


class NoMatchError(AssertionError):
    ROBOT_SUPPRESS_NAME = True

    def __init__(self, expected, timeout, output=None):
        self.expected = expected
        self.timeout = secs_to_timestr(timeout)
        self.output = output
        super().__init__(self._get_message())

    def _get_message(self):
        expected = (
            f"'{self.expected}'"
            if isinstance(self.expected, str)
            else seq2str(self.expected, lastsep=" or ")
        )
        msg = f"No match found for {expected} in {self.timeout}."
        if self.output is not None:
            msg += " Output:\n" + self.output
        return msg