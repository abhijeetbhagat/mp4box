from mp4box.box import AVC1Box
from mp4box.parsing.btrt import parse_btrt
from mp4box.utils.exceptions import InvalidBoxError

def parse_avc1(reader, my_size):
    box = AVC1Box(my_size)
    cnt = 0
    while not reader.reached_eof() and cnt < my_size:
        size = reader.read32()
        type = reader.read32_as_str()
        cnt += size
        if type == 'avcC':
            box.avcc = parse_avcc(reader, size)
        elif type == 'btrt':
            box.btrt = parse_btrt(reader, size)
        else:
            raise InvalidBoxError("type % is unknown" % type, None)

    return box



