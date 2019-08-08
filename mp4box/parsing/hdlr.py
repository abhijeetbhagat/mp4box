
def parse_hdlr(self, size):
    version = self.reader.read32()
    box = HandlerBox(size, version, 0)
    box.predefined = self.reader.read32()
    box.handler_type = self.reader.read32_as_str()
    box.reserved.append(self.reader.read32())
    box.reserved.append(self.reader.read32())
    box.reserved.append(self.reader.read32())
    box.name = self.reader.readn_as_str(size - 32)
    self.boxes['unknown'] = {}
    self.boxes['unknown']['hdlr'] = box 
