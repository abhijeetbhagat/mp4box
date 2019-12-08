from mp4box.box import MP4AudioBox


def parse_mp4a(reader, my_size):
    box = MP4AudioBox(my_size)
    reader.skip(my_size - 8)
    return box
