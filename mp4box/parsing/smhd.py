from mp4box.box import SoundMediaHeaderBox


def parse_smhd(reader, my_size):
    box = SoundMediaHeaderBox(my_size)
    reader.skip(my_size - 8)
    return box
