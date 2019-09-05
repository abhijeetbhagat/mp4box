from mp4box.box import EditListBox

def parse_elst(reader, size):
    version = reader.read32()
    box = EditListBox(size, version) 
    entry_count = reader.read32()
    for _ in range(0..entry_count):
        if version == 1:
            box.segment_duration.append(reader.read64())
            box.media_time.append(reader.read64())
        else:
            box.segment_duration.append(reader.read32())
            box.media_time.append(reader.read32()) 

        box.media_rate_integer.append(reader.read16())
        box.media_rate_fraction.append(reader.read16())

    return box
