
def parse_edts(reader, my_size):
    size = reader.read32()
    type = reader.read32_as_str()
    if type is 'elts':
        elts = parse_elts(self, size)
    else:
        raise InvalidBoxError("type %s unknown")
