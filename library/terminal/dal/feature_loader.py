# 📁 common/feature_loader.py

import importlib
import yaml
import os
from robot.libraries.BuiltIn import BuiltIn

class FeatureLoader:
    def __init__(self, feature_name, feature_module_path="library.terminal.dal.feature", spec_directory=None):
        self.feature = feature_name              # ví dụ: "gpon"
        self.module_path = feature_module_path   # ví dụ: "features"
        self.spec_directory = spec_directory or os.path.join(os.path.dirname(__file__), "spec")
        self._instance = None

    def load(self):
        if self._instance:
            return self._instance

        # Bước 1: Lấy API từ CustomTelnet đã connect
        telnet = BuiltIn().get_library_instance("CustomTelnet")
        device_info = telnet._cache.current.device_info  # Đảm bảo đã gán trong connect_to_dut()
        api = device_info['api']

        # Bước 2: Load file spec YAML tương ứng
        spec_path = os.path.abspath(os.path.join(self.spec_directory, f"{api}.yaml"))
        if not os.path.exists(spec_path):
            raise FileNotFoundError(f"Spec file '{spec_path}' not found for API '{api}'")

        with open(spec_path, 'r') as f:
            spec = yaml.safe_load(f)

        # Bước 3: Tìm class name trong feature tương ứng
        feature_map = spec.get('feature', {})
        class_name = feature_map.get(self.feature)
        if not class_name:
            raise ValueError(f"Feature '{self.feature}' not defined in spec for API '{api}'")

        # Bước 4: Import module và khởi tạo class
        module = importlib.import_module(f"{self.module_path}.{self.feature}")
        cls = getattr(module, class_name)
        self._instance = cls()
        return self._instance