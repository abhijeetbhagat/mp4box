from mp4box.box import BitRateBox

def parse_btrt(reader, size):
    box = BitRateBox(size)
    box.buffer_size_db = reader.read32()
    box.max_bitrate = reader.read32()
    box.avg_bitrate = reader.read32()
