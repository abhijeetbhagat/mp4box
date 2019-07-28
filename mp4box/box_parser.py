class BoxParser:
    def __init__(self, file):
        self.reader = StreamReader(file)

    def parse(self):
        size = self.reader.read32()
        type = self.reader.read32_as_str()
        while True:
            if type is 'ftyp':
                self.parse_ftyp(size)
            elif type is 'moov':
                self.parse_moov(size)
            else:
                raise InvalidBoxError("type %s unknown" % type)
            #At the end of current box parsing, the file pointer will be
            #ready to read the size and type of the next box
            size = self.reader.read32()
            type = self.reader.read32_as_str()

    def parse_ftyp(self, size):
        major_brand = self.reader.read32_as_str()
        minor_version = self.reader.read32()
        compatible_brands = []
        cnt = size - 16
        while cnt < size - 4:
            compatible_brands.append(self.reader.read32_as_str())
            cnt += 4
        box = FileTypeBox(size, 'ftyp', major_brand, minor_version, compatible_brands)

    def parse_moov(self, size):
        pass
