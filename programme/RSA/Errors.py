class Error(Exception):
    pass

class RSAKeyError(Error):
    def __init__(self , message):
        self.message = message

class GCDError(Error):
    def __init__(self, message):
        self.message = message

class RSAEncryptionError(Error):
    def __init__(self, message):
        self.message = message

class RSAMessageError(Error):
    def __init__(self, message):
        self.message = message

class RSADecryptionError(Error):
    def __init__(self, message):
        self.message = message

class RSAError(Error):
    def __init__(self, message):
        self.message = message
