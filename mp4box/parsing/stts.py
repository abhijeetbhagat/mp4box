from mp4box.box import TimeToSampleBox

def parse_stts(reader, size):
    entry_count = reader.read32()
    box = TimeToSampleBox(size, 0, 0)
    box.entry_count = entry_count
    for _ in range(0, entry_count):
        box.sample_count.append(reader.read32())
        box.sample_delta.append(reader.read32())
