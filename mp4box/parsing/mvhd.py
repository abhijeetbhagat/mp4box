
def parse_mvhd(self, size): 
    version = self.reader.read32()
    box = MovieHeaderBox(size, version, 0)
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
    
    self.reader.skip(76)
    box.next_track_id = self.reader.read32()
    self.boxes['unknown'] = {}
    self.boxes['unknown']['mvhd'] = box 
