from mp4box.box import TimeToSampleBox

def parse_stts(reader, size):
    version = reader.read32()
    box = TimeToSampleBox(size, version, 0)
    box.entry_count = reader.read32()
    for _ in range(0, box.entry_count):
        box.sample_count.append(reader.read32())
        box.sample_delta.append(reader.read32())
    return box
