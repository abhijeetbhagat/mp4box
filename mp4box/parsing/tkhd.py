
def parse_tkhd(self, size):
    version = self.reader.read8()
    flags = self.reader.readn_as_int(3)
    box = TrackHeaderBox(size, version, 0)
    if version == 0:
        box.creation_time = self.reader.read32()
        box.modification_time = self.reader.read32()
        box.track_id = self.reader.read32()
        box.reserved1 = self.reader.read32()
        box.duration = self.reader.read32()
    else:
        box.creation_time = self.reader.read64()
        box.modification_time = self.reader.read64()
        box.track_id = self.reader.read32()
        box.reserved1 = self.reader.read32()
        box.duration = self.reader.read64()

    box.reserved2.append(self.reader.read32())
    box.reserved2.append(self.reader.read32())
    box.layer = self.reader.read16()
    box.alternate_group = self.reader.read16()
    vol =  box.volume = self.reader.read16()
    #if track is audio, then set volume to 1 else 0
    #for now, set it to 0 until we figure how to check the track type
    box.volume = 0
    box.reserved3 = self.reader.read16()
    self.reader.skip(36)
    #TODO abhi - width and height values are stored as fixed point 16.16 values
    #not sure how to convert that to float at this point in time. But reading 
    #the first 16 bits and treating them as a value does the job.
    box.width = self.reader.read16()
    self.reader.skip(2)
    box.height = self.reader.read16()
    self.reader.skip(2)
    self.boxes['unknown'] = {}
    self.boxes['unknown']['tkhd'] = box 
