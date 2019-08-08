
def parse_stts(self, size):
    entry_count = self.reader.read32()
    box = TimeToSampleBox(size, 0, 0)
    box.entry_count = entry_count
    for _ in range(0, entry_count):
        box.sample_count.append(self.reader.read32())
        box.sample_delta.append(self.reader.read32())
