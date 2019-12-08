from mp4box.box import CompositionTimeToSampleBox


def parse_ctts(reader, my_size):
    version = reader.read32()
    box = CompositionTimeToSampleBox(my_size, version, 0)
    box.entry_count = reader.read32()
    for _ in range(0, box.entry_count):
        box.sample_count.append(reader.read32())
        box.sample_offset.append(reader.read32())

    return box
