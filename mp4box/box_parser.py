class BoxParser:
    def __init__(self, file):
        self.reader = StreamReader(file)

    def parse(self):
        size = self.reader.read32()
        type = self.reader.read32_as_str()
        if type is 'ftyp':
            self.parse_ftyp(size)

    def parse_ftyp(self, size):
        major_brand = self.reader.read32_as_str()
        minor_version = self.reader.read32()
        compatible_brands = []
        cnt = size - 16
        while cnt < size:
            compatible_brands.append(self.reader.read32_as_str())
            cnt += 4
        box = FileTypeBox(size, 'ftyp', major_brand, minor_version, compatible_brands)
