class Box:
    def __init__(self, size: int, box_type: int, uuid):
        self.size = size
        self.type = box_type
        self.uuid = uuid

class FullBox(Box):
    def __init__(self, size: int, box_type: int, uuid, v: int, f: int):
        super().__init__(size, box_type, uuid)
        #Boxes with an unrecognized version shall be ignored and skipped. 
        self.version = v
        self.flags = f
