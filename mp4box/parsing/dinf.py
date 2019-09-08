from mp4box.box import DataInformationBox
from mp4box.parsing.dref import parse_dref
from mp4box.utils.exceptions import InvalidBoxError

def parse_dinf(reader, my_size):
    box = DataInformationBox(my_size)
    cnt = 8
    while not reader.reached_eof() and cnt < my_size:
        size = reader.read32()
        type = reader.read32_as_str()
        cnt += size
        if type == 'dref':
            box.dref = parse_dref(reader, size)
        else:
            raise InvalidBoxError('type %s unknown' % type, None)

    return box
