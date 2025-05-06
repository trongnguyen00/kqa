from robot.api.deco import keyword

class IxiaSession:
    def __init__(self, base):
        self.base = base

    @keyword