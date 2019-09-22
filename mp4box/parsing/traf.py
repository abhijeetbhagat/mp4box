from mp4box.box import TrackFragmentBox
from mp4box.parsing.tfdt import parse_tfdt
from mp4box.parsing.tfhd import parse_tfhd
from mp4box.parsing.trun import parse_trun
from mp4box.utils.exceptions import InvalidBoxError

def parse_traf(reader, my_size):
    box = TrackFragmentBox(reader, my_size)
    cnt = 8
    while not reader.reached_eof() and cnt < my_size:
        size = reader.read32()
        type = reader.read32_as_str()
        cnt += size
        if type == 'tfhd':
            box.tfhd = parse_tfhd(reader, size)
        elif type == 'tfdt':
            box.tfdt = parse_tfdt(reader, size)
        elif type == 'trun':
            box.trun.append(parse_trun(reader, size))
        else:
            raise InvalidBoxError("type %s unknown" % type, None)

    return box
