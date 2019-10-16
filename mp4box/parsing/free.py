from mp4box.box import FreeSpaceBox

def parse_free(reader, size):
    data = reader.readn(size - 8)
    box = FreeSpaceBox(size, data)
    return box

