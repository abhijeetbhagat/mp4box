
def parse_stsz(self, size):
    box = SampleSizeBox(size, 0, 0)
    box.sample_size = self.reader.read32()
    box.sample_count = self.reader.read32()
    if box.sample_size:
        for _ in range(0, box.sample_count):
            box.entry_size.append(self.reader.read32())
