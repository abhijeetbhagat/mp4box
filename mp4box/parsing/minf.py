from mp4box.box import MediaInformationBox
from mp4box.parsing.stbl import parse_stbl
from mp4box.parsing.dinf import parse_dinf
from mp4box.parsing.vmhd import parse_vmhd 
from mp4box.parsing.smhd import parse_smhd 
from mp4box.utils.exceptions import InvalidBoxError

def parse_minf(reader, my_size):
    box = MediaInformationBox(my_size)
    cnt = 8
    while not reader.reached_eof() and cnt < my_size:
        size = reader.read32()
        type = reader.read32_as_str()
        cnt += size
        if type == 'vmhd':
            box.vmhd = parse_vmhd(reader, size)
        elif type == 'dinf':
            box.dinf = parse_dinf(reader, size)
        elif type == 'stbl':
            box.stbl = parse_stbl(reader, size)
        elif type == 'smhd':
            box.smhd = parse_smhd(reader, size)
        else:
            raise InvalidBoxError("type %s unknown" % type, None)

    return box

