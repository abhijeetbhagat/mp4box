from mp4box.box import MediaBox
from mp4box.parsing.minf import parse_minf
from mp4box.parsing.mdhd import parse_mdhd
from mp4box.parsing.hdlr import parse_hdlr
from mp4box.utils.exceptions import InvalidBoxError

def parse_mdia(self, my_size):
    box = MediaBox(my_size)
    cnt = 0
    while not reader.reached_eof() and cnt < my_size:
        size = reader.read32()
        type = reader.read32_as_str()
        cnt += size
        if type == 'mdhd':
            box.mdhd = parse_mdhd()
        elif type == 'hdlr':
            box.hdlr = parse_hdlr()
        elif type == 'minf':
            box.minf = parse_minf()
        else:
            raise InvalidBoxError("type % unknown")
        
    return box
