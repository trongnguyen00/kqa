from robot.api.deco import keyword
from ixia.commands.media import MediaCommands

class MediaKeywords:
    def __init__(self, base):
        self.cmd = MediaCommands(base)

    @keyword
    def get_list_media_type(self, port_handle):
        return self.cmd.get_list_media_type(port_handle)

    @keyword
    def set_media_type(self, port_handle, media_type):
        return self.cmd.set_media_type(port_handle, media_type)

    @keyword
    def get_list_modules(self):
        return self.cmd.get_list_modules()

    @keyword
    def list_module_types(self, module_number):
        return self.cmd.list_module_types(module_number)

    @keyword
    def set_module_types(self, module_number, module_type):
        return self.cmd.set_module_types(module_number, module_type)