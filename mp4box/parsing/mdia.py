from mp4box.box import MediaBox
from mp4box.parsing.minf import parse_minf
from mp4box.parsing.mdhd import parse_mdhd
from mp4box.parsing.hdlr import parse_hdlr

def parse_mdia(self, my_size):
    box = MediaBox(my_size)
    cnt = 0
    while not reader.reached_eof() and cnt < my_size:
        size = reader.read32()
        type = reader.read32_as_str()
        cnt += size
        if type is 'mdhd':
            box.mdhd = parse_mdhd()
        elif type is 'hdlr':
            box.hdlr = parse_hdlr()
        elif type is 'minf':
            box.minf = parse_minf()
        else:
            raise InvalidBoxError("type % unknown")
        
    return box
