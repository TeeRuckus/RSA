class Error(Exception):
    pass

class RSAKeyError(Error):
    def __init__(self , message):
        self.message = message
