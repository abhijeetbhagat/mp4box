from mp4box.box import MediaHeaderBox

def parse_mdhd(reader, size): 
    version = reader.read32()
    box = MediaHeaderBox(size, version, 0)
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
    
    data = reader.readn_as_int(2)
    box.pad = (data >> 15) & 1
    language = data & 0x7fff
    box.language = chr(97 + (language >> 10) - 1 %97) + \
                   chr(97 + (language >> 5 & 0x1f) - 1 % 97) + \
                   chr(97 + (language & 0x1f) - 1 % 97)
    box.predefined = reader.read16()
    return box
