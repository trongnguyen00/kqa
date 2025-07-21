import yaml
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn

class CustomField:
    def __init__(self, data):
        for k, v in (data or {}).items():
            setattr(self, k, v)

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
        self.connections = CustomField(info.get("connections", {}))
        self.custom = CustomField(info.get("custom", {}))


class Topology:
    def __init__(self):
        self._device_ports = {}

    def add_ports(self, device_name, port_type, ports):
        if device_name not in self._device_ports:
            self._device_ports[device_name] = []
        for p in ports:
            port = Port(
                name=p.get("name"),
                index=p.get("index"),
                alias=p.get("alias"),
                link=p.get("link"),
                port_type=port_type
            )
            self._device_ports[device_name].append(port)

    def get_ports(self, device_name):
        return self._device_ports.get(device_name, [])

    def get_ports_by_type(self, device_name, port_type):
        return [p for p in self.get_ports(device_name) if p.type == port_type]

    def get_port_by_link(self, device_name, link):
        for port in self.get_ports(device_name):
            if port.link == link:
                return port
        raise AssertionError(f"Link '{link}' not found on device '{device_name}'")

    def get_port_by_alias(self, device_name, alias):
        for port in self.get_ports(device_name):
            if port.alias == alias:
                return port
        raise AssertionError(f"Alias '{alias}' not found on device '{device_name}'")

    def get_port_by_name(self, device_name, name):
        for port in self.get_ports(device_name):
            if port.name == name:
                return port
        raise AssertionError(f"Port name '{name}' not found on device '{device_name}'")


class TopologyLoader:
    def __init__(self):
        self.devices = {}
        self.topology = Topology()
        self.topology_data = None

    @keyword
    def load_topology(self, yaml_file_path):
        try:
            with open(yaml_file_path, 'r') as f:
                self.topology_data = yaml.safe_load(f)
        except Exception as e:
            raise AssertionError(f"Failed to load topology file: {str(e)}")

        for device_name, info in self.topology_data.get("devices", {}).items():
            self.devices[device_name] = Device(name=device_name, info=info)

        for device_name, port_groups in self.topology_data.get("topology", {}).items():
            for port_type, ports in port_groups.items():
                self.topology.add_ports(device_name, port_type, ports)

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
        return [vars(p) for p in self.topology.get_ports(device_name)]

    @keyword
    def get_ports_by_type(self, device_name, port_type):
        return [vars(p) for p in self.topology.get_ports_by_type(device_name, port_type)]

    @keyword
    def get_port_name_from_link(self, device_name, link):
        return self.topology.get_port_by_link(device_name, link).name

    @keyword
    def get_port_index_from_link(self, device_name, link):
        return self.topology.get_port_by_link(device_name, link).index

    @keyword
    def get_port_alias_from_link(self, device_name, link):
        return self.topology.get_port_by_link(device_name, link).alias

    @keyword
    def get_port_name_from_alias(self, device_name, alias):
        return self.topology.get_port_by_alias(device_name, alias).name

    @keyword
    def get_port_index_from_alias(self, device_name, alias):
        return self.topology.get_port_by_alias(device_name, alias).index

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
        return self.get_device(device_name).connections.ip

    @keyword
    def get_device_custom_field(self, device_name, field):
        return getattr(self.get_device(device_name).custom, field, None)

    @keyword
    def get_device_connection_field(self, device_name, field):
        return getattr(self.get_device(device_name).connections, field, None)

    @keyword
    def get_full_device_info(self, device_name):
        device = self.get_device(device_name)
        return {
            "name": device.name,
            "type": device.type,
            "api": device.api,
            "model": device.model,
            "connections": vars(device.connections),
            "custom": vars(device.custom)
        }

    @keyword
    def get_port_object_by_link(self, device_name, link):
        return self.topology.get_port_by_link(device_name, link)

    @keyword
    def get_port_object_by_alias(self, device_name, alias):
        return self.topology.get_port_by_alias(device_name, alias)

    @keyword
    def get_all_port_objects(self, device_name):
        return self.topology.get_ports(device_name)
