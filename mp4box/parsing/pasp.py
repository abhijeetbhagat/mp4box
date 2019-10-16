from mp4box.box import PixelAspectRatioBox

def parse_pasp(reader, my_size):
    box = PixelAspectRatioBox(my_size)
    #TODO abhi: for now, just skip the colr box data
    reader.skip(my_size - 8)
    return box


