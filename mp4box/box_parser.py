from mp4box.box import RootBox
from mp4box.parsing.ftyp import parse_ftyp
from mp4box.parsing.moov import parse_moov
from mp4box.parsing.free import parse_free
from mp4box.parsing.mdat import parse_mdat
from mp4box.utils.stream_reader import StreamReader
from mp4box.utils.exceptions import InvalidBoxError

class BoxParser:
    def __init__(self, file):
        self.reader = StreamReader(file)
        #TODO abhi: should this be a dict or a RootBox type?
        self.boxes = {}
        self.root = RootBox()

    def parse(self):
        size = self.reader.read32()
        type = self.reader.read32_as_str()
        while not self.reader.reached_eof():
            if type == 'ftyp':
                self.root.ftyp = parse_ftyp(self.reader, size)
            elif type == 'moov':
                self.root.moov = parse_moov(self.reader, size)
            elif type == 'free':
                self.root.free = parse_free(self.reader, size)
            elif type == 'mdat':
                self.root.mdat = parse_mdat(self.reader, size)
            else:
                raise InvalidBoxError("type %s unknown" % type, None)
            if self.reader.reached_eof():
                break
            #At the end of current box parsing, the file pointer will be
            #ready to read the size and type of the next box
            size = self.reader.read32()
            type = self.reader.read32_as_str()

        #Either box parsing was successful or it has errors

    def get_boxes(self):
        return self.boxes
