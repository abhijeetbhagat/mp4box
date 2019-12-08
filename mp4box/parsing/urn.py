from mp4box.box import DataEntryUrnBox


def parse_urn(reader, my_size):
    box = DataEntryUrnBox(my_size)
    return box
