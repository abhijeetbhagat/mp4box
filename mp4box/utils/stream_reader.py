from io import BufferedReader

class StreamReader:
    def __init__(self, file):
        self.stream = open(file, "rb")

    def __del__(self):
        self.stream.close()

    def read8(self):
        return stream.read(1)

    def read32(self):
        return int.from_bytes(stream.read(4)[0:], "big")

    def read32_as_str(self):
        return stream.read(4)[0:].decode('utf-8')
