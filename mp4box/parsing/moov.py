from mp4box.box import MovieBox

def parse_moov(reader, my_size):
    box = MovieBox(my_size)
    cnt = 0
    while not reader.reached_eof() and cnt < my_size:
        size = reader.read32()
        type = reader.read32()
        cnt += size
        if type is 'mvhd':
            parse_mvhd(reader, size)
        elif type is 'trak': 
            parse_trak(reader, size)
        elif type is 'iods': 
            raise NotImplementedError
        else:
            raise InvalidBoxError("type %s unknown" % type, None)

    return box
