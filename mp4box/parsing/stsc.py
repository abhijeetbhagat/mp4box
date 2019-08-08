from mp4box.box import SampleToChunkBox

def parse_stsc(reader, size):
    entry_count = reader.read32()
    box = SampleToChunkBox(size, 0, 0)
    box.entry_count = entry_count
    for _ in range(0, entry_count):
        box.first_chunk.append(reader.read32())
        box.samples_per_chunk.append(reader.read32())
        box.sample_description_index.append(reader.read32())
