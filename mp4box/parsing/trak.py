from mp4box.box import TrackBox
from mp4box.parsing.tkhd import parse_tkhd
from mp4box.parsing.edts import parse_edts
from mp4box.parsing.mdia import parse_mdia
from mp4box.utils.exceptions import InvalidBoxError

def parse_trak(reader, my_size):
    box = TrackBox(my_size)
    cnt = 8
    while not reader.reached_eof() and cnt < my_size:
        size = reader.read32()
        type = reader.read32_as_str()
        cnt += size
        if type == 'tkhd':
            box.tkhd = parse_tkhd(reader, size)
        elif type == 'edts':
            box.edts = parse_edts(reader, size)
        elif type == 'mdia':
            box.mdia = parse_mdia(reader, size)
        else:
            raise InvalidBoxError("type %s unknown" % type, None)

    return box
