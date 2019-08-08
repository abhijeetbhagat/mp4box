from mp4box.parsing.ftyp import parse_ftyp
from mp4box.parsing.moov import parse_moov
from mp4box.parsing.free import parse_free
from mp4box.utils.stream_reader import StreamReader
from mp4box.utils.exceptions import InvalidBoxError

class BoxParser:
    def __init__(self, file):
        self.reader = StreamReader(file)
        #TODO abhi: should this be a dict or a RootBox type?
        self.boxes = {}
        self.root = []

    def parse(self):
        size = self.reader.read32()
        type = self.reader.read32_as_str()
        while True:
            if type == 'ftyp':
                box['ftyp'] = parse_ftyp(self.reader, size)
            elif type == 'moov':
                box['moov'] = parse_moov(self.reader, size)
            elif type == 'free':
                box['free'] = parse_free(self.reader, size)
            elif type == 'mdat':
                raise NotImplementedError
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
