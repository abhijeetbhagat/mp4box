from mp4box.box import TrackFragmentDecodingTime

def parse_tfdt(reader, my_size):
    version = reader.read32()
    box = TrackFragmentDecodingTime(my_size, version, flags)
    if version == 1:
        box.base_media_decode_time = reader.read64()
    else:
        box.base_media_decode_time = reader.read32()
