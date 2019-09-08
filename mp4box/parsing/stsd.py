from mp4box.box import SampleDescriptionBox
from mp4box.parsing.avc1 import parse_avc1

def parse_stsd(reader, my_size):
    version = reader.read32()
    box = SampleDescriptionBox(my_size, version, 0)
    box.entry_count = reader.read32()
    size = reader.read32()
    type = reader.read32_as_str()
    box.avc1 = parse_avc1(reader, size)
    return box
