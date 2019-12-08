from mp4box.box import MediaDataBox


def parse_mdat(reader, my_size):
    box = MediaDataBox(my_size, reader.current_pos())
    # we have nothing to do with media data as of now
    # and advancing the file ptr is necessary
    reader.skip(my_size - 8)
    return box
