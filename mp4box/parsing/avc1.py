from mp4box.box import AVC1Box
from mp4box.parsing.avcc import parse_avcc
from mp4box.parsing.btrt import parse_btrt
from mp4box.parsing.colr import parse_colr
from mp4box.parsing.pasp import parse_pasp
from mp4box.utils.exceptions import InvalidBoxError

def parse_avc1(reader, my_size):
    box = AVC1Box(my_size)
    reader.skip(6) #reserved
    box.data_ref_index = reader.read16()
    box.vid_enc_version = reader.read16()
    box.vid_enc_revision_lvl = reader.read16()
    box.vid_enc_vendor = reader.read32_as_str()
    box.vid_temporal_quality = reader.read32()
    box.vid_spatial_quality = reader.read32()
    box.vid_frame_pixel_size = reader.read32()
    box.vid_resolution = reader.read64()
    box.vid_data_size = reader.read32()
    box.vid_frame_count = reader.read16()
    box.vid_enc_name_len = reader.read8()
    box.vid_enc_name = reader.readn_as_str(box.vid_enc_name_len)

    if box.vid_enc_name_len < 31:
        #if the encoder name is less than 31, then pad with 0s
        box.vid_enc_name = box.vid_enc_name + '0' * (31 - box.vid_enc_name_len)
        reader.skip(31 - box.vid_enc_name_len)

    box.vid_pixel_depth = reader.read16()
    box.vid_color_tbl_id = reader.read16()

    cnt = 86 #avc1 len + name + number of bytes parsed above

    while not reader.reached_eof() and cnt < my_size:
        size = reader.read32()
        type = reader.read32_as_str()
        cnt += size
        if type == 'avcC':
            box.avcc = parse_avcc(reader, size)
        elif type == 'btrt':
            box.btrt = parse_btrt(reader, size)
        elif type == 'colr':
            box.colr = parse_colr(reader, size)
        elif type == 'pasp':
            box.pasp = parse_pasp(reader, size)
        else:
            raise InvalidBoxError("type %s is unknown" % type, None)

    return box



