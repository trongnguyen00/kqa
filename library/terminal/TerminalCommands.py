import yaml
import re
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from kqa.Telnet import CustomTelnet

class TerminalCommands:
    def __init__(self):
        self.telnet = BuiltIn().get_library_instance('CustomTelnet')
        self.current_prompt_level = 0

    @keyword
    def send_commands_from_group(self, file_path, command_group, **variables):
        """
        Send commands from a specific group in a YAML file over Telnet.
        Example:
        ${value}                      Create Dictionary                             mapper_value=1    uni_value=1
        Send Commands From Group      /home/ats/ATS/kqa/suites/resource/dut.yaml    show-all-vlan     &{value}
        
        dut.yaml example:
        ---
        commands:
          show-all-vlan:
            - model: default
              shell: |
                traffic-profile trongnk_test modify
                  tcont 1
                    gemport 1/1
                    dba-profile GPON_BE
                  mapper 1
                    gemport count 1
                  bridge 1
                    ani mapper {{mapper_value}}
                    uni virtual-eth {{uni_value}}
                      extended-vlan-tagging-operation s-202t
                  apply
                !
                class-map dscp_46
                 match dscp 46
                 match ip any any any
                !
        """
        # Load YAML file
        with open(file_path, 'r') as file:
            yaml_data = yaml.safe_load(file)

        # Get commands from the specified group
        commands = yaml_data['commands'][command_group][0]['shell'].splitlines()

        # Replace variables in commands
        commands = self._replace_variables_in_commands(commands, variables)

        # Send commands
        for line in commands:
            line = line.strip()
            if not line or line == '!':
                self._adjust_prompt_level(0)
                continue

            indentation_level = self._get_indentation_level(line)
            command = self._strip_indentation(line)

            # Adjust prompt level
            self._adjust_prompt_level(indentation_level)

            # Execute command
            self._execute_command(command)

        # Exit to base prompt
        self._adjust_prompt_level(0)

    def _replace_variables_in_commands(self, commands, variables):
        """
        Replace variables in the commands with the provided values.
        """
        processed_commands = []
        for command in commands:
            for key, value in variables.items():
                command = command.replace(f"{{{{{key}}}}}", str(value))
            processed_commands.append(command)
        return processed_commands

    def _get_indentation_level(self, line):
        """
        Calculate the indentation level of a line.
        """
        stripped_line = line.lstrip()
        return len(line) - len(stripped_line)

    def _strip_indentation(self, line):
        """
        Remove leading spaces from a line.
        """
        return line.lstrip()

    def _adjust_prompt_level(self, target_level):
        """
        Adjust the prompt level by sending 'exit' or updating the prompt.
        """
        while self.current_prompt_level > target_level:
            self.telnet.write('exit')
            self._update_prompt()
            self.current_prompt_level -= 1

        while self.current_prompt_level < target_level:
            self._update_prompt()
            self.current_prompt_level += 1

    def _execute_command(self, command):
        """
        Send a command over Telnet and handle errors.
        """
        self.telnet.write(command)
        output = self.telnet.read_until_regexp(r"(#|>)")
        if "% Invalid input detected" in output:
            raise RuntimeError(f"Command failed: {command}\nOutput: {output}")

    def _update_prompt(self):
        """
        Update the current prompt by reading until the next prompt.
        """
        prompt = self.telnet.read_until_regexp(r"(#|>)").strip()
        self.telnet.set_prompt(prompt)