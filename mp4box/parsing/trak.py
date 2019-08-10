from mp4box.box import TrackBox
from mp4box.parsing.tkhd import parse_tkhd
from mp4box.parsing.edts import parse_edts
from mp4box.parsing.mdia import parse_mdia

def parse_trak(reader, my_size):
    box = TrackBox(reader, my_size)
    cnt = 0
    while not reader.reached_eof() and cnt < my_size:
        size = reader.read32()
        type = reader.read32_as_str()
        cnt += size
        if type is 'tkhd':
            box.tkhd = parse_tkhd(reader, size)
        elif type is 'edts':
            box.edts = parse_edts(reader, size)
        elif type is 'mdia':
            box.mdia = parse_mdia(reader, size)
        else:
            raise InvalidBoxError("type %s unknown")
