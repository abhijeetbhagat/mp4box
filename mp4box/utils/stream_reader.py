import os
from io import BufferedReader

class StreamReader:
    def __init__(self, file):
        if isinstance(file, str):
            self.stream = open(file, "rb")
        else:
            self.stream = file
        self.size = os.path.getsize(self.stream.name)

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, type, val, tb):
        self.close()

    def close(self):
        if self.stream:
            self.stream.close()
            self.stream = None

    def reset(self):
        self.seek(0)

    def read8(self):
        #TODO abhi: umm do we need to do this?
        return int.from_bytes(self.stream.read(1), "big")

    def read16(self):
        return int.from_bytes(self.stream.read(2), "big")

    def read32(self):
        return int.from_bytes(self.stream.read(4), "big")

    def read32_as_str(self):
        return str(self.stream.read(4)[0:], 'utf-8')

    def read64(self):
        return int.from_bytes(self.stream.read(8), "big") 

    def readn(self, n: int):
        return self.stream.read(n)

    def readn_as_int(self, n: int):
        return int.from_bytes(self.stream.read(n), "big")

    def readn_as_str(self, n):
        return str(self.stream.read(n)[0:], 'utf-8', 'ignore')

    def skip(self, n: int):
        self.stream.read(n)

    def current_pos(self):
        return self.stream.tell()

    def reached_eof(self):
        #TODO abhi: should calculate size of the file in the ctor and
        #check if tell() has crossed it
        return self.stream.peek(1) == b''
