
from mp4box.box import TrackHeaderBox

def parse_tkhd(reader, size):
    version = reader.read8()
    flags = reader.readn_as_int(3)
    box = TrackHeaderBox(size, version, 0)
    if version == 0:
        box.creation_time = reader.read32()
        box.modification_time = reader.read32()
        box.track_id = reader.read32()
        box.reserved1 = reader.read32()
        box.duration = reader.read32()
    else:
        box.creation_time = reader.read64()
        box.modification_time = reader.read64()
        box.track_id = reader.read32()
        box.reserved1 = reader.read32()
        box.duration = reader.read64()

    box.reserved2.append(reader.read32())
    box.reserved2.append(reader.read32())
    box.layer = reader.read16()
    box.alternate_group = reader.read16()
    vol =  box.volume = reader.read16()
    #if track is audio, then set volume to 1 else 0
    #for now, set it to 0 until we figure how to check the track type
    box.volume = 0
    box.reserved3 = reader.read16()
    reader.skip(36)
    #TODO abhi - width and height values are stored as fixed point 16.16 values
    #not sure how to convert that to float at this point in time. But reading 
    #the first 16 bits and treating them as a value does the job.
    box.width = reader.read16()
    reader.skip(2)
    box.height = reader.read16()
    reader.skip(2)
    boxes['unknown'] = {}
    boxes['unknown']['tkhd'] = box 
