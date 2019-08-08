
def parse_stsc(self, size):
    entry_count = self.reader.read32()
    box = SampleToChunkBox(size, 0, 0)
    box.entry_count = entry_count
    for _ in range(0, entry_count):
        box.first_chunk.append(self.reader.read32())
        box.samples_per_chunk.append(self.reader.read32())
        box.sample_description_index.append(self.reader.read32())
