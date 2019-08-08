
def parse_elst(self, size):
    version = self.reader.read32()
    box = EditListBox(size, version) 
    entry_count = self.reader.read32()
    for _ in range(0..entry_count):
        if version == 1:
            box.segment_duration.append(self.reader.read64())
            box.media_time.append(self.reader.read64())
        else:
            box.segment_duration.append(self.reader.read32())
            box.media_time.append(self.reader.read32()) 

        box.media_rate_integer.append(self.reader16())
        box.media_rate_fraction.append(self.reader16())
