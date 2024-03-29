class FatalError(Exception):
    def __init__(self, msg: str, debug_msg: str):
        super().__init__(msg)
        self.debug_msg = debug_msg
