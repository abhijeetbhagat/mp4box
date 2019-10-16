from mp4box.box import PLEPBox

def parse_plep(reader, my_size):
    box = PLEPBox(my_size)
    reader.skip(my_size - 8)
    return box


