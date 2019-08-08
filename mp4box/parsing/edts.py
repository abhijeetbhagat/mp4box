
def parse_edts(self, my_size):
    size = self.reader.read32()
    type = self.reader.read32()
    if type is 'elts':
        parse_elts(self, size)
    else:
        raise InvalidBoxError("type %s unknown")
