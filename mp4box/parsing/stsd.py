from mp4box.box import SampleDescriptionBox
from mp4box.parsing.avc1 import parse_avc1

def parse_stsd(reader, my_size):
    box = SampleDescriptionBox(my_size)
    size = reader.read32()
    type = reader.read32_as_str()
    box.avc1 = parse_avc1(reader, size)
    return box
