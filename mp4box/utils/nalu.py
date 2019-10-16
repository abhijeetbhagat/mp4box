class NALU:
    def __init__(self, size, reader):
        self.data = reader.readn(size)
        self.type = None
        self.size = size
