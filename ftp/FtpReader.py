class FtpReader:
    """Placeholder for bytes pdf read from ftp server"""

    def __init__(self):
        self.data: bytes = b''

    def read(self, new_data: bytes):
        self.data += new_data

    def clear(self):
        self.data = b''
