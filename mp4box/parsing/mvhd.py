from mp4box.box import MovieHeaderBox

def parse_mvhd(reader, size): 
    version = reader.read32()
    box = MovieHeaderBox(size, version, 0)
    if version == 0:
        box.creation_time = reader.read32()
        box.modification_time = reader.read32()
        box.timescale = reader.read32()
        box.duration = reader.read32() 
    else:
        box.creation_time = reader.read64()
        box.modification_time = reader.read64()
        box.timescale = reader.read32()
        box.duration = reader.read64()
    
    reader.skip(76)
    box.next_track_id = reader.read32()
    boxes['unknown'] = {}
    boxes['unknown']['mvhd'] = box 
