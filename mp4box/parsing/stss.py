from mp4box.box import SyncSampleBox

def parse_stss(reader, size):
    version = reader.read32()
    box = SyncSampleBox(size, 0, 0)
    box.entry_count = reader.read32()
    for _ in range(0, box.entry_count):
        box.sample_number.append(reader.read32())

    return box
