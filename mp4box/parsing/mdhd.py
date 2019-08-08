
def parse_mdhd(self, size): 
    version = self.reader.read32()
    box = MediaHeaderBox(size, version, 0)
    if version == 0:
        box.creation_time = self.reader.read32()
        box.modification_time = self.reader.read32()
        box.timescale = self.reader.read32()
        box.duration = self.reader.read32() 
    else:
        box.creation_time = self.reader.read64()
        box.modification_time = self.reader.read64()
        box.timescale = self.reader.read32()
        box.duration = self.reader.read64()
    
    data = self.reader.readn_as_int(2)
    box.pad = (data >> 15) & 1
    language = data & 0x7fff
    box.language = chr(97 + (language >> 10) - 1 %97) + \
                   chr(97 + (language >> 5 & 0x1f) - 1 % 97) + \
                   chr(97 + (language & 0x1f) - 1 % 97)
    box.predefined = self.reader.read16()
    self.boxes['unknown'] = {}
    self.boxes['unknown']['mdhd'] = box 
