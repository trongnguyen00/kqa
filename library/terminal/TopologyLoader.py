import yaml
from robot.api.deco import keyword

class Port:
    def __init__(self, name, index=None, alias=None, link=None, port_type=None):
        self.name = name
        self.index = index
        self.alias = alias
        self.link = link
        self.type = port_type

    def __repr__(self):
        return f"Port(name={self.name}, index={self.index}, alias={self.alias}, link={self.link}, type={self.type})"


class Device:
    def __init__(self, name, info):
        self.name = name
        self.type = info.get("type")
        self.api = info.get("api")
        self.model = info.get("model")
        self.connections = info.get("connections", {})
        self.custom = info.get("custom", {})
        self.ports = []

    def add_port(self, port: Port):
        self.ports.append(port)

    def get_ports_by_type(self, port_type):
        return [p for p in self.ports if p.type == port_type]

    def get_port_by_link(self, link):
        for port in self.ports:
            if port.link == link:
                return port
        raise AssertionError(f"Link '{link}' not found on device '{self.name}'")

    def get_port_by_alias(self, alias):
        for port in self.ports:
            if port.alias == alias:
                return port
        raise AssertionError(f"Alias '{alias}' not found on device '{self.name}'")

    def get_port_by_name(self, name):
        for port in self.ports:
            if port.name == name:
                return port
        raise AssertionError(f"Port name '{name}' not found on device '{self.name}'")


class TopologyLoader:
    def __init__(self):
        self.devices = {}
        self.topology_data = None
        self.topology_links = {}

    @keyword
    def load_topology(self, yaml_file_path):
        try:
            with open(yaml_file_path, 'r') as f:
                self.topology_data = yaml.safe_load(f)
        except Exception as e:
            raise AssertionError(f"Failed to load topology file: {str(e)}")

        for device_name, info in self.topology_data.get("devices", {}).items():
            device = Device(name=device_name, info=info)

            conn_ports = self.topology_data.get("topology", {}).get(device_name, {})
            self.topology_links[device_name] = conn_ports

            for port_type in ['ethernet', 'pon']:
                ports = conn_ports.get(port_type, [])
                for p in ports:
                    port = Port(
                        name=p.get("name"),
                        index=p.get("index"),
                        alias=p.get("alias"),
                        link=p.get("link"),
                        port_type=port_type
                    )
                    device.add_port(port)

            self.devices[device_name] = device

    @keyword
    def get_device(self, device_name):
        if device_name not in self.devices:
            raise AssertionError(f"Device '{device_name}' not found.")
        return self.devices[device_name]

    @keyword
    def get_connection_info(self, device_name):
        return self.get_device(device_name).connections

    @keyword
    def get_all_devices(self):
        return list(self.devices.keys())

    @keyword
    def get_all_ports_of_device(self, device_name):
        return [vars(p) for p in self.get_device(device_name).ports]

    @keyword
    def get_ports_by_type(self, device_name, port_type):
        return [vars(p) for p in self.get_device(device_name).get_ports_by_type(port_type)]

    @keyword
    def get_port_name_from_link(self, device_name, link):
        return self.get_device(device_name).get_port_by_link(link).name

    @keyword
    def get_port_index_from_link(self, device_name, link):
        return self.get_device(device_name).get_port_by_link(link).index

    @keyword
    def get_port_alias_from_link(self, device_name, link):
        return self.get_device(device_name).get_port_by_link(link).alias

    @keyword
    def get_port_name_from_alias(self, device_name, alias):
        return self.get_device(device_name).get_port_by_alias(alias).name

    @keyword
    def get_port_index_from_alias(self, device_name, alias):
        return self.get_device(device_name).get_port_by_alias(alias).index

    @keyword
    def get_device_api(self, device_name):
        return self.get_device(device_name).api

    @keyword
    def get_device_type(self, device_name):
        return self.get_device(device_name).type

    @keyword
    def get_device_model(self, device_name):
        return self.get_device(device_name).model

    @keyword
    def get_device_ip(self, device_name):
        return self.get_device(device_name).connections.get("ip")

    @keyword
    def get_device_custom_field(self, device_name, field):
        return self.get_device(device_name).custom.get(field)

    @keyword
    def get_full_device_info(self, device_name):
        device = self.get_device(device_name)
        return {
            "name": device.name,
            "type": device.type,
            "api": device.api,
            "model": device.model,
            "connections": device.connections,
            "custom": device.custom,
            "ports": [vars(p) for p in device.ports]
        }

    @keyword
    def get_topology_links(self, device_name):
        return self.topology_links.get(device_name, {})
