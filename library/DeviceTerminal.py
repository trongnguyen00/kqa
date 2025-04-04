import yaml

class DeviceTerminal(object):

    def __init__(self):
        """Initialize without a predefined topology YAML file."""
        self.topology = None

    def load_topology(self, yaml_file_path):
        """Load the topology YAML file.

        Args:
            yaml_file_path (str): The path to the topology YAML file.
        """
        try:
            with open(yaml_file_path, 'r') as file:
                self.topology = yaml.safe_load(file)
        except Exception as e:
            raise AssertionError(f"Failed to load topology file: {str(e)}")

    def get_device_info(self, device_name):
        """Get device information from the loaded topology.

        Args:
            device_name (str): The name of the device (e.g., 'Switch0').

        Returns:
            dict: A dictionary containing the device's information.

        Raises:
            AssertionError: If the device is not found in the topology.
        """
        if self.topology is None:
            raise AssertionError("Topology is not loaded. Call 'load_topology' first.")

        devices = self.topology.get('devices', {})
        if device_name not in devices:
            raise AssertionError(f"Device '{device_name}' not found in topology.")

        return devices[device_name]

