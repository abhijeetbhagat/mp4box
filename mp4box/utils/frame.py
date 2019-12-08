class Frame:
    def __init__(self, size):
        self.type = None  # whether this is an audio/video frame
        self.data = None  # this is the raw frame data
        self.codec = None  # codec
        self.time_stamp = 0  # TS of the frame
        self.size = size


class AudioFrame(Frame):
    def __init__(self):
        return super().__init__()


class VideoFrame(Frame):
    def __init__(self, size, reader):
        super().__init__(size)
        self.data = reader.readn(size)
