from mp4box.box import SampleToChunkBox


def parse_stsc(reader, size):
    version = reader.read32()
    box = SampleToChunkBox(size, version, 0)
    box.entry_count = reader.read32()
    for _ in range(0, box.entry_count):
        box.first_chunk.append(reader.read32())
        box.samples_per_chunk.append(reader.read32())
        box.sample_description_index.append(reader.read32())

    return box
