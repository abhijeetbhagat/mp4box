from mp4box.box import FileTypeBox
from mp4box.utils.stream_reader import StreamReader
from mp4box.utils.exceptions import InvalidBoxError

class BoxParser:
    def __init__(self, file):
        self.reader = StreamReader(file)
        self.boxes = {}

    def parse(self):
        size = self.reader.read32()
        type = self.reader.read32_as_str()
        while True:
            if type == 'ftyp':
                self.parse_ftyp(size)
            elif type == 'moov':
                self.parse_moov(size)
            else:
                raise InvalidBoxError("type %s unknown" % type, None)
            if self.reader.reached_eof():
                break
            #At the end of current box parsing, the file pointer will be
            #ready to read the size and type of the next box
            size = self.reader.read32()
            type = self.reader.read32_as_str()

        #Either box parsing was successful or it has errors

    def parse_ftyp(self, size):
        major_brand = self.reader.read32_as_str()
        minor_version = self.reader.read32()
        compatible_brands = []
        cnt = size - 16
        while cnt < size - 4:
            compatible_brands.append(self.reader.read32_as_str())
            cnt += 4
        box = FileTypeBox(size, major_brand, minor_version, compatible_brands)
        self.boxes['ftyp'] = box

    def parse_moov(self, size):
        pass

    def get_boxes(self):
        return self.boxes
