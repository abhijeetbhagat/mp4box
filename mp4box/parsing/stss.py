
def parse_stss(self, size):
    entry_count = self.reader.read32()
    box = SyncSampleBox(size, 0, 0)
    box.entry_count = entry_count
    for _ in range(0, entry_count):
        box.sample_number.append(self.reader.read32())
