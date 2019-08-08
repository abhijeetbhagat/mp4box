from mp4box.box import ChunkOffsetBox

def parse_stco(reader, size):
    box = ChunkOffsetBox(size, 0, 0)
    box.entry_count = reader.read32()
    for _ in range(0, box.entry_count):
        box.chunk_offset.append(reader.read32())
    return box
