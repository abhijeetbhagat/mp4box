
def parse_trak(self, my_size):
    size = self.reader.read32()
    type = self.reader.read32()
    cnt = 0
    while cnt < my_size:
        if type is 'tkhd':
            parse_tkhd()
        elif type is 'edts':
            parse_edts()
        elif type is 'mdia':
            parse_mdia()
        else:
            raise InvalidBoxError("type %s unknown")
