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

    def get_connection_info(self, device_name):
        """Get connnection information from the loaded topology.

        Args:
            device_name (str): The name of the device (e.g., 'Switch0').

        Returns:
            dict: A dictionary containing the device's information.

        Raises:
            AssertionError: If the device is not found in the topology.
        """
        if self.topology is None:
            raise AssertionError("Topology is not loaded. Call 'load_topology' first.")

        connections = self.topology.get('topology', {})
        if device_name not in connections:
            raise AssertionError(f"Device '{device_name}' not found in topology.")

        return connections[device_name]

    def get_port_name_from_link(self, device_name, port_link):
        """Get port name from link information.

        Args:
            device_name (str): The name of the device (e.g., 'Olt0').
            port_link (str): The link information (e.g., 'olt0-ixia-1').

        Returns:
            str: The port name.

        Raises:
            AssertionError: If the device or port link is not found in the topology.
        """
        if self.topology is None:
            raise AssertionError("Topology is not loaded. Call 'load_topology' first.")

        connections = self.topology.get('topology', {})
        if device_name not in connections:
            raise AssertionError(f"Device '{device_name}' not found in topology.")

        device_connections = connections[device_name]
        for port_type in ['ethernet', 'pon']:
            ports = device_connections.get(port_type, [])
            for port in ports:
                if port.get('link') == port_link:
                    return port.get('name')

        raise AssertionError(f"Port link '{port_link}' not found in device '{device_name}'.")

    def get_port_alias_from_link(self, device_name, port_link):
        """Get port alias from link information.

        Args:
            device_name (str): The name of the device (e.g., 'Olt0').
            port_link (str): The link information (e.g., 'olt0-ixia-1').

        Returns:
            str: The port alias.

        Raises:
            AssertionError: If the device or port link is not found in the topology.
        """
        if self.topology is None:
            raise AssertionError("Topology is not loaded. Call 'load_topology' first.")

        connections = self.topology.get('topology', {})
        if device_name not in connections:
            raise AssertionError(f"Device '{device_name}' not found in topology.")

        device_connections = connections[device_name]
        for port_type in ['ethernet', 'pon']:
            ports = device_connections.get(port_type, [])
            for port in ports:
                if port.get('link') == port_link:
                    return port.get('alias')

        raise AssertionError(f"Port link '{port_link}' not found in device '{device_name}'.")

    
    