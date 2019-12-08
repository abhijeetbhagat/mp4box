from mp4box.box import SampleTableBox
from mp4box.parsing.stsd import parse_stsd
from mp4box.parsing.ctts import parse_ctts
from mp4box.parsing.stts import parse_stts
from mp4box.parsing.stss import parse_stss
from mp4box.parsing.stsc import parse_stsc
from mp4box.parsing.stsz import parse_stsz
from mp4box.parsing.stco import parse_stco
from mp4box.utils.exceptions import InvalidBoxError


def parse_stbl(reader, my_size):
    box = SampleTableBox(my_size)
    cnt = 8
    while not reader.reached_eof() and cnt < my_size:
        size = reader.read32()
        type = reader.read32_as_str()
        cnt += size
        if type == "stsd":
            box.stsd = parse_stsd(reader, size)
        elif type == "stts":
            box.stts = parse_stts(reader, size)
        elif type == "ctts":
            box.ctts = parse_ctts(reader, size)
        elif type == "stss":
            box.stss = parse_stss(reader, size)
        elif type == "stsc":
            box.stsc = parse_stsc(reader, size)
        elif type == "stsz":
            box.stsz = parse_stsz(reader, size)
        elif type == "stco":
            box.stco = parse_stco(reader, size)
        else:
            raise InvalidBoxError("type %s is unknown" % type, None)

    return box
