from mp4box.box import DataEntryUrlBox

def parse_url(reader, my_size):
    flags = reader.read32()
    box = DataEntryUrlBox(my_size, 0, flags)
    return box
    
