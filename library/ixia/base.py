import subprocess
import threading
import time

class TclBase:
    def __init__(self):
        self.process = None
        self.output_lock = threading.Lock()

    def start_process(self):
        if self.process is not None:
            raise RuntimeError("Already connected to Tclsh.")
        self.process = subprocess.Popen(
            ["tclsh8.6"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            bufsize=0
        )

    def stop_process(self):
        if self.process:
            with self.output_lock:
                self.process.stdin.write("exit\n")
                self.process.stdin.flush()
                self.process.wait(timeout=5)
                self.process = None

    def send_tcl_command(self, command, timeout=10):
        """Sends a command to the Tclsh process and waits for the output.
        1. command: the command to be sent to tclsh.
        2. timeout: time to wait for the command to finish.
        3. return: the output of the command.
        unless, please using send_line to send command without get output.
        """
        with self.output_lock:
            wrapped = f"set __robot_output [{command}]\nputs $__robot_output\n"
            self.process.stdin.write(wrapped)
            self.process.stdin.flush()
            start_time = time.time()
            while True:
                if time.time() - start_time > timeout:
                    raise TimeoutError(f"Timeout on command: {command}")
                line = self.process.stdout.readline()
                if line:
                    return line.strip()

    def send_line(self, line):
        """Sends a line to the Tclsh process without waiting for output.
        """
        self.process.stdin.write(line + "\n")
        self.process.stdin.flush()
        self.process.stdout.readline()

    def send_line_and_wait_marker(self, line, marker="<<<READY>>>", timeout=100, poll_interval=5):
        """Sends a line to the Tclsh process and waits for a specific marker in the output.
        Default timeout is 100 seconds.
        Default poll interval is 5 seconds.
        """
        self.process.stdin.write(line + "\n")
        self.process.stdin.write(f'puts "{marker}"\n')
        self.process.stdin.flush()
        output_lines = []
        start_time = time.time()
        while True:
            if time.time() - start_time > timeout:
                raise TimeoutError("Timeout waiting for command to complete.")
            line_out = self.process.stdout.readline()
            if not line_out:
                continue
            line_out = line_out.strip()
            output_lines.append(line_out)
            if marker in line_out:
                break
            time.sleep(poll_interval)
        return "\n".join(output_lines)
