from mp4box.box import AVCCConfigurationBox

def parse_avcc(reader, my_size):
    box = AVCCConfigurationBox(my_size)
    #TODO abhi: implement avcC parsing
    box.config_version = reader.read8()
    box.profile_indication = reader.read8()
    box.profile_compatibility = reader.read8()
    box.level_indication = reader.read8()
    box.len_size_minus_one = reader.read8() & 3

    box.num_sps = reader.read8() & 0x1f 
    for _ in range(0, box.num_sps):
        box.sps_len.append(reader.read16())
        box.sps_nalu.extend(reader.readn(box.sps_len[-1]))

    box.num_pps = reader.read8()
    for _ in range(0, box.num_pps):
        box.pps_len.append(reader.read16())
        box.pps_nalu.extend(reader.readn(box.pps_len[-1]))

    return box
