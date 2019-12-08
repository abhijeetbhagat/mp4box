from mp4box.box import MovieFragmentBox
from mp4box.parsing.mfhd import parse_mfhd
from mp4box.parsing.traf import parse_traf
from mp4box.utils.exceptions import InvalidBoxError


def parse_moof(reader, my_size):
    box = MovieFragmentBox(my_size)
    cnt = 8
    while not reader.reached_eof() and cnt < my_size:
        size = reader.read32()
        type = reader.read32_as_str()
        cnt += size
        if type == "mfhd":
            box.mvhd = parse_mfhd(reader, size)
        elif type == "traf":
            box.traf = parse_traf(reader, size)
        else:
            raise InvalidBoxError("type %s unknown" % type, None)

    return box
