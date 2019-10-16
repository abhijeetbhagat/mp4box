from mp4box.box import UserDataBox

def parse_udta(reader, my_size):
    box = UserDataBox(my_size)
    reader.skip(my_size - 8)
    return box


