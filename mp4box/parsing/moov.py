from mp4box.box import MovieBox
from mp4box.parsing.iods import parse_iods
from mp4box.parsing.trak import parse_trak
from mp4box.parsing.mvhd import parse_mvhd
from mp4box.parsing.udta import parse_udta
from mp4box.utils.exceptions import InvalidBoxError

def parse_moov(reader, my_size):
    box = MovieBox(my_size)
    cnt = 8
    while not reader.reached_eof() and cnt < my_size:
        size = reader.read32()
        type = reader.read32_as_str()
        cnt += size
        if type == 'mvhd':
            box.mvhd = parse_mvhd(reader, size)
        elif type == 'trak': 
            box.traks.append(parse_trak(reader, size))
        elif type == 'iods': 
            box.iods = parse_iods(reader, size)
        elif type == 'udta':
            box.udta = parse_udta(reader, size)
        else:
            raise InvalidBoxError("type %s unknown" % type, None)

    return box
