from mp4box.box import SampleDescriptionBox
from mp4box.parsing.avc1 import parse_avc1
from mp4box.parsing.mp4a import parse_mp4a
from mp4box.utils.exceptions import InvalidBoxError


def parse_stsd(reader, my_size):
    version = reader.read32()
    box = SampleDescriptionBox(my_size, version, 0)
    box.entry_count = reader.read32()
    size = reader.read32()
    type = reader.read32_as_str()
    if type == "avc1":
        box.avc1 = parse_avc1(reader, size)
    elif type == "mp4a":
        box.mp4a = parse_mp4a(reader, size)
    else:
        raise InvalidBoxError("type %s unknown" % type, None)

    return box
