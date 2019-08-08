
def parse_mdia(self, my_size):
    size = self.reader.read32()
    type = self.reader.read32()
    cnt = 0
    while cnt < my_size:
        if type is 'mdhd':
            parse_mdhd()
        elif type is 'hdlr':
            parse_hdlr()
        elif type is 'minf':
            parse_minf()
        else:
            raise InvalidBoxError("type % unknown")
