from mp4box.box import DataReferenceBox
from mp4box.parsing.url import parse_url

def parse_dref(reader, my_size):
    box = DataReferenceBox(my_size)
    cnt = 0
    while not reader.reached_eof() and cnt < my_size:
        size = reader.read32()
        type = reader.read32_as_str()
        if type is 'url':
            #TODO abhi: not implemented right now
            #box.url = parse_url()
            raise NotImplementedError
        else:
            raise InvalidBoxError('type %s unknown' % type, None)

    return box
