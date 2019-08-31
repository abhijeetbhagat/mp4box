class VideoSample:
    def __init__(self, size, reader):
        super().__init__(size)
        self.data = reader.readn(size)
