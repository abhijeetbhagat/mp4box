from mp4box.box import MediaBox

def parse_mdia(self, my_size):
    size = self.reader.read32()
    type = self.reader.read32()
    cnt = 0
    box = MediaBox(size)
    while cnt < my_size:
        if type is 'mdhd':
            box.mdhd = parse_mdhd()
        elif type is 'hdlr':
            box.hdlr = parse_hdlr()
        elif type is 'minf':
            box.minf = parse_minf()
        else:
            raise InvalidBoxError("type % unknown")
        
    return box
