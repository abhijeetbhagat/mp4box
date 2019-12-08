from mp4box.box import TrackFragmentHeaderBox


def parse_tfhd(reader, my_size):
    flags = reader.read32()
    box = TrackFragmentHeaderBox(my_size, 0, flags)
    box.track_id = reader.read32()
    # we've already parsed 8 bytes before this function call
    # and we've parsed 8 bytes above.
    cnt = 16
    box.base_data_offset = reader.read64()
    cnt += 8
    if cnt < my_size:  # the following are optional according to the doc
        box.sample_description_index = reader.read32()
        box.default_sample_duration = reader.read32()
        box.default_sample_size = reader.read32()
        box.default_sample_flag = reader.read32()

    return box
