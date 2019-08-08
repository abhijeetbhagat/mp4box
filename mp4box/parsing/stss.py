from mp4box.box import SyncSampleBox

def parse_stss(reader, size):
    entry_count = reader.read32()
    box = SyncSampleBox(size, 0, 0)
    box.entry_count = entry_count
    for _ in range(0, entry_count):
        box.sample_number.append(reader.read32())

    return box
