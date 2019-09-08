from mp4box.box import DataReferenceBox
from mp4box.parsing.url import parse_url
from mp4box.utils.exceptions import InvalidBoxError

def parse_dref(reader, my_size):
    version = reader.read32()
    box = DataReferenceBox(my_size, version, 0)
    box.entry_count = reader.read32()
    cnt = 16 #dref len + name + version + entry_count
    while not reader.reached_eof() and cnt < my_size:
        size = reader.read32()
        type = reader.read32_as_str()
        cnt += size
        if type == 'url ':
            #TODO abhi: not implemented right now
            #box.url = parse_url()
            box.data_entries.append(parse_url(reader, size))
        elif type == 'urn ':
            #TODO abhi: call the parse_urn() function here
            raise NotImplementedError
        else:
            raise InvalidBoxError('type %s unknown' % type, None)

    return box
