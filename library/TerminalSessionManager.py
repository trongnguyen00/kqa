from abc import ABC, abstractmethod
from typing import Dict, Optional, Any, List
from dataclasses import dataclass
from robot.api.deco import keyword
import telnetlib
import subprocess
import time
import threading
import logging

@dataclass
class SessionInfo:
    """Class for storing session metadata"""
    session_id: int
    connection_type: str
    host: str
    port: int
    username: str
    password: str
    is_connected: bool
    current_prompt: str
    last_command: str
    last_output: str
    created_at: float
    last_activity: float

class TerminalSession(ABC):
    """Abstract base class for terminal sessions"""
    
    def __init__(self, session_id: int, host: str, port: int, username: str, password: str):
        self.session_id = session_id
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.is_connected = False
        self.current_prompt = ""
        self.last_command = ""
        self.last_output = ""
        self.created_at = time.time()
        self.last_activity = time.time()
        self._lock = threading.Lock()

    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to the terminal"""
        pass

    @abstractmethod
    def disconnect(self) -> bool:
        """Close the terminal connection"""
        pass

    @abstractmethod
    def send_command(self, command: str, reset_prompt: bool = False, timeout: Optional[int] = None) -> str:
        """Send a command to the terminal and return the output"""
        pass

    @abstractmethod
    def expect(self, pattern: str, timeout: Optional[int] = None) -> bool:
        """Wait for a specific pattern in the output"""
        pass

    def get_session_info(self) -> SessionInfo:
        """Return session metadata"""
        return SessionInfo(
            session_id=self.session_id,
            connection_type=self.__class__.__name__,
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            is_connected=self.is_connected,
            current_prompt=self.current_prompt,
            last_command=self.last_command,
            last_output=self.last_output,
            created_at=self.created_at,
            last_activity=self.last_activity
        )

class TelnetSession(TerminalSession):
    """Telnet session implementation"""
    
    def __init__(self, session_id: int, host: str, port: int, username: str, password: str):
        super().__init__(session_id, host, port, username, password)
        self.telnet = None

    def connect(self) -> bool:
        try:
            self.telnet = telnetlib.Telnet(self.host, self.port)
            self.telnet.read_until(b"login: ")
            self.telnet.write(self.username.encode('ascii') + b"\n")
            self.telnet.read_until(b"Password: ")
            self.telnet.write(self.password.encode('ascii') + b"\n")
            self.is_connected = True
            self.current_prompt = self._get_prompt()
            return True
        except Exception as e:
            logging.error(f"Telnet connection failed: {str(e)}")
            return False

    def disconnect(self) -> bool:
        if self.telnet:
            self.telnet.close()
            self.is_connected = False
            return True
        return False

    def send_command(self, command: str, reset_prompt: bool = False, timeout: Optional[int] = None) -> str:
        with self._lock:
            if not self.is_connected:
                raise RuntimeError("Not connected to terminal")
            
            self.last_command = command
            self.telnet.write(command.encode('ascii') + b"\n")
            
            if timeout:
                output = self.telnet.read_until(self.current_prompt.encode('ascii'), timeout=timeout)
            else:
                output = self.telnet.read_until(self.current_prompt.encode('ascii'))
            
            self.last_output = output.decode('ascii')
            self.last_activity = time.time()
            
            if reset_prompt:
                self.current_prompt = self._get_prompt()
            
            return self.last_output

    def expect(self, pattern: str, timeout: Optional[int] = None) -> bool:
        try:
            if timeout:
                output = self.telnet.read_until(pattern.encode('ascii'), timeout=timeout)
            else:
                output = self.telnet.read_until(pattern.encode('ascii'))
            return True
        except Exception:
            return False

    def _get_prompt(self) -> str:
        self.telnet.write(b"\n")
        output = self.telnet.read_until(b"\n")
        return output.decode('ascii').strip()

class TclshSession(TerminalSession):
    """Tclsh session implementation"""
    
    def __init__(self, session_id: int, host: str, port: int, username: str, password: str):
        super().__init__(session_id, host, port, username, password)
        self.process = None

    def connect(self) -> bool:
        try:
            self.process = subprocess.Popen(
                ["tclsh"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                bufsize=0
            )
            self.is_connected = True
            self.current_prompt = "% "
            return True
        except Exception as e:
            logging.error(f"Tclsh connection failed: {str(e)}")
            return False

    def disconnect(self) -> bool:
        if self.process:
            self.process.terminate()
            self.is_connected = False
            return True
        return False

    def send_command(self, command: str, reset_prompt: bool = False, timeout: Optional[int] = None) -> str:
        with self._lock:
            if not self.is_connected:
                raise RuntimeError("Not connected to terminal")
            
            self.last_command = command
            self.process.stdin.write(command + "\n")
            self.process.stdin.flush()
            
            output = []
            start_time = time.time()
            
            while True:
                if timeout and time.time() - start_time > timeout:
                    raise TimeoutError(f"Command timeout: {command}")
                
                line = self.process.stdout.readline()
                if not line:
                    break
                
                output.append(line)
                if line.strip() == self.current_prompt:
                    break
            
            self.last_output = "".join(output)
            self.last_activity = time.time()
            return self.last_output

    def expect(self, pattern: str, timeout: Optional[int] = None) -> bool:
        start_time = time.time()
        while True:
            if timeout and time.time() - start_time > timeout:
                return False
            
            line = self.process.stdout.readline()
            if pattern in line:
                return True
            if not line:
                return False

class TerminalSessionManager:
    """Robot Framework library for managing terminal sessions"""
    
    def __init__(self):
        self.sessions: Dict[int, TerminalSession] = {}
        self.current_session_id: Optional[int] = None
        self._session_counter = 0
        self._lock = threading.Lock()

    @keyword
    def create_telnet_session(self, host: str, port: int = 23, username: str = "", password: str = "") -> int:
        """Create a new Telnet session"""
        with self._lock:
            session_id = self._get_next_session_id()
            session = TelnetSession(session_id, host, port, username, password)
            if session.connect():
                self.sessions[session_id] = session
                if self.current_session_id is None:
                    self.current_session_id = session_id
                return session_id
            raise RuntimeError(f"Failed to create Telnet session to {host}:{port}")

    @keyword
    def create_tclsh_session(self) -> int:
        """Create a new Tclsh session"""
        with self._lock:
            session_id = self._get_next_session_id()
            session = TclshSession(session_id, "localhost", 0, "", "")
            if session.connect():
                self.sessions[session_id] = session
                if self.current_session_id is None:
                    self.current_session_id = session_id
                return session_id
            raise RuntimeError("Failed to create Tclsh session")

    @keyword
    def switch_session(self, session_id: int) -> bool:
        """Switch to a different session"""
        with self._lock:
            if session_id in self.sessions:
                self.current_session_id = session_id
                return True
            return False

    @keyword
    def send_command(self, command: str, reset_prompt: bool = False, timeout: Optional[int] = None) -> str:
        """Send a command to the current session"""
        if self.current_session_id is None:
            raise RuntimeError("No active session")
        return self.sessions[self.current_session_id].send_command(command, reset_prompt, timeout)

    @keyword
    def expect(self, pattern: str, timeout: Optional[int] = None) -> bool:
        """Wait for a pattern in the current session"""
        if self.current_session_id is None:
            raise RuntimeError("No active session")
        return self.sessions[self.current_session_id].expect(pattern, timeout)

    @keyword
    def get_session_info(self, session_id: Optional[int] = None) -> Dict[str, Any]:
        """Get information about a session"""
        if session_id is None:
            session_id = self.current_session_id
        if session_id is None or session_id not in self.sessions:
            raise RuntimeError("Invalid session ID")
        return self.sessions[session_id].get_session_info().__dict__

    @keyword
    def disconnect_session(self, session_id: Optional[int] = None) -> bool:
        """Disconnect a session"""
        if session_id is None:
            session_id = self.current_session_id
        if session_id is None or session_id not in self.sessions:
            return False
        
        with self._lock:
            session = self.sessions.pop(session_id)
            if session_id == self.current_session_id:
                self.current_session_id = next(iter(self.sessions), None)
            return session.disconnect()

    @keyword
    def disconnect_all_sessions(self) -> bool:
        """Disconnect all sessions"""
        success = True
        for session_id in list(self.sessions.keys()):
            if not self.disconnect_session(session_id):
                success = False
        return success

    def _get_next_session_id(self) -> int:
        self._session_counter += 1
        return self._session_counter 