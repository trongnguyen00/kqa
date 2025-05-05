from robot.api.deco import keyword

class IxiaMedia:
    def __init__(self, base):
        self.base = base

    @keyword
    def get_list_media_type(self, port_handle):
        return self.base.send_command(f"AgtInvoke AgtPhysicalInterface ListAvailableMediaTypes {port_handle}")

    @keyword
    def set_media_type(self, port_handle, media_type):
        return self.base.send_command(f"AgtInvoke AgtPhysicalInterface SetMediaType {port_handle} {media_type}")
