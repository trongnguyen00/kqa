class MediaCommands:
    def __init__(self, base):
        self.base = base

    def get_list_media_type(self, port_handle):
        return self.base.send_tcl_command(f"AgtInvoke AgtPhysicalInterface ListAvailableMediaTypes {port_handle}")

    def set_media_type(self, port_handle, media_type):
        return self.base.send_tcl_command(f"AgtInvoke AgtPhysicalInterface SetMediaType {port_handle} {media_type}")

    def get_list_modules(self):
        return self.base.send_tcl_command("AgtInvoke AgtPortSelector ListModules")

    def list_module_types(self, module_number):
        return self.base.send_tcl_command(f"AgtInvoke AgtPortSelector ListModuleTypes {module_number}")

    def set_module_types(self, module_number, module_type):
        return self.base.send_tcl_command(f"AgtInvoke AgtPortSelector SetModuleType {module_number} {module_type}")
