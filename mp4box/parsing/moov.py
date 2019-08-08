from mp4box.box import MovieBox

def parse_moov(reader, my_size):
    box = MovieBox(my_size)
    cnt = 0
    while not reader.reached_eof() and cnt < my_size:
        size = reader.read32()
        type = reader.read32_as_str()
        cnt += size
        if type is 'mvhd':
            mvhd = parse_mvhd(reader, size)
        elif type is 'trak': 
            trak = parse_trak(reader, size)
        elif type is 'iods': 
            raise NotImplementedError
        else:
            raise InvalidBoxError("type %s unknown" % type, None)

    return box
