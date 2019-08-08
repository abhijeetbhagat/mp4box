
def parse_stco(self, size):
    box = ChunkOffsetBox(size, 0, 0)
    box.entry_count = self.reader.read32()
    for _ in range(0, box.entry_count):
        box.chunk_offset.append(self.reader.read32())
