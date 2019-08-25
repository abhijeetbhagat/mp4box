from mp4box.box import ChunkOffsetBox

def parse_stco(reader, size):
    version = reader.read32()
    box = ChunkOffsetBox(size, version, 0)
    box.entry_count = reader.read32()
    for _ in range(0, box.entry_count):
        box.chunk_offsets.append(reader.read32())
    return box
