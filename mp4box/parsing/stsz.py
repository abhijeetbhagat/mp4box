from mp4box.box import SampleSizeBox

def parse_stsz(reader, my_size):
    version = reader.read32()
    box = SampleSizeBox(my_size, version, 0)
    box.sample_size = reader.read32()
    box.sample_count = reader.read32()
    if box.sample_size == 0:
        for _ in range(0, box.sample_count):
            box.entry_size.append(reader.read32())

    return box
