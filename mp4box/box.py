class Box:
    def __init__(self, size: int, box_type: str, uuid):
        self.size = size
        self.type = box_type
        self.uuid = uuid

class FullBox(Box):
    def __init__(self, size: int, box_type: str, uuid, v: int, f: int):
        super().__init__(size, box_type, uuid)
        #Boxes with an unrecognized version shall be ignored and skipped. 
        self.version = v
        self.flags = f

class FileTypeBox(Box):
    def __init__(self, size: int, major_brand: int, minor_version: int, compatible_brands: [int]):
        super().__init__(size, 'ftyp')
        self.major_brand = major_brand
        self.minor_brand = minor_version
        self.compatible_brands = compatible_brands
