
def parse_vmhd(self, size):
    self.reader.read32()
    box = VideoMediaHeaderBox(size, 0, 1)
    box.graphics_mode = self.reader.reader16()
    box.opcolor.append(self.reader.reader16())
    box.opcolor.append(self.reader.reader16())
    box.opcolor.append(self.reader.reader16()) 
