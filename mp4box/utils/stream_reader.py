from io import BufferedReader

class StreamReader:
    def __init__(self, file):
        if isinstance(file, str):
            self.stream = open(file, "rb")
        else:
            self.stream = file

    #def __del__(self):
    #    self.stream.close()

    def read8(self):
        return self.stream.read(1)

    def read32(self):
        return int.from_bytes(self.stream.read(4), "big")

    def read32_as_str(self):
        return self.stream.read(4)[0:].decode('utf-8')

    def readn(self, n: int):
        return self.stream.read(n)

    def reached_eof(self):
        #TODO abhi: should calculate size of the file in the ctor and
        #check if tell() has crossed it
        return self.stream.peek(1) == b''
