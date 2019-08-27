from mp4box.box import SampleTableBox
from mp4box.parsing.stsd import parse_stsd
from mp4box.parsing.ctts import parse_ctts
from mp4box.parsing.stts import parse_stts
from mp4box.parsing.stss import parse_stss
from mp4box.parsing.stsc import parse_stsc
from mp4box.parsing.stsz import parse_stsz
from mp4box.parsing.stco import parse_stco

def parse_stbl(reader, my_size):
    box = SampleTableBox(my_size, )
    cnt = 0
    while not reader.reached_eof() and cnt < my_size:
        size = reader.read32()
        type = reader.read32_as_str()
        cnt += size
        if type is 'stsd':
            box.stsd = parse_stsd(reader, size)
        elif type is 'stts':
            box.stts = parse_stts(reader, size)
        elif type is 'ctts':
            box.ctts = parse_ctts(reader, size)
        elif type is 'stss':
            box.stss = parse_stss(reader, size)
        elif type is 'stsc':
            box.stsc = parse_stsc(reader, size)
        elif type is 'stsz':
            box.stsz = parse_stsz(reader, size)
        elif type is 'stco':
            box.stco = parse_stco(reader, size)
        else:
            raise InvalidBoxError()

    return box
