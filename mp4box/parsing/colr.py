from mp4box.box import ColourInformationBox

def parse_colr(reader, my_size):
    box = ColourInformationBox(my_size)
    #TODO abhi: for now, just skip the colr box data
    reader.skip(my_size - 8)
    return box


