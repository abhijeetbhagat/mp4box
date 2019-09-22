from mp4box.box import TrackFragmentRunBox

def parse_trun(reader, my_size):
    flags = reader.read32()
    box = TrackFragmentRunBox(my_size, 0, flags)

    box.sample_count = reader.read32()
    cnt = 16 #we have parsed 8 bytes before function call and then 8
    if cnt < my_size:
        box.data_offset = 0
        box.first_sample_flags = 0
        for _ in range(0, box.sample_count):
            entry = TrackFragmentRunBox.Entry()
            entry.sample_duration = reader.read32()
            entry.sample_size = reader.read32()
            entry.sample_flags = reader.read32()
            entry.sample_composition_time_offset = reader.reader32()

        box.entries.append()

    return box
