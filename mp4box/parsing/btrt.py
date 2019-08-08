
def parse_btrt(self, size):
    box = BitRateBox(size)
    box.buffer_size_db = self.reader.read32()
    box.max_bitrate = self.reader.read32()
    box.avg_bitrate = self.reader.read32()
