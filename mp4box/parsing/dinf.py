from mp4box.box import DataInformationBox
from mp4box.parsing.dref import parse_dref()

def parse_dinf(reader, my_size):
    box = DataInformationBox(my_size)
    cnt = 0
    while not reader.reached_eof() and cnt < my_size:
        size = reader.read32()
        type = reader.read32_as_str()
        if type is 'dref':
            box.dref = parse_dref()
        else:
            raise InvalidBoxError('type %s unknown' % type, None)

    return box
