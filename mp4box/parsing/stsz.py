from mp4box.box import SampleSizeBox

def parse_stsz(reader, size):
    box = SampleSizeBox(size, 0, 0)
    box.sample_size = reader.read32()
    box.sample_count = reader.read32()
    if box.sample_size:
        for _ in range(0, box.sample_count):
            box.entry_size.append(reader.read32())
