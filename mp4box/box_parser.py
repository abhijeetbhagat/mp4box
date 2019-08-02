from mp4box.box import FileTypeBox
from mp4box.box import MovieBox
from mp4box.box import FreeSpaceBox
from mp4box.box import MovieHeaderBox
from mp4box.box import TrackHeaderBox
from mp4box.box import MediaHeaderBox
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
            elif type == 'mvhd':
                self.parse_mvhd(size)
            elif type == 'tkhd':
                self.parse_tkhd(size)
            elif type == 'mdhd':
                self.parse_mdhd(size)
            elif type == 'free':
                self.parse_free(size)
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
        cnt = 0
        while cnt < size + 4 - 16 - 4:
            compatible_brands.append(self.reader.read32_as_str())
            cnt += 4
        box = FileTypeBox(size, major_brand, minor_version, compatible_brands)
        self.boxes['ftyp'] = box

    def parse_moov(self, size):
        while True:
            pass
        box = MovieBox(size)
        self.boxes['moov'] = box
        
    def parse_free(self, size):
        data = self.reader.readn(size - 4)
        box = FreeSpaceBox(size, data)
        self.boxes['free'] = box

    def parse_mvhd(self, size): 
        version = self.reader.read32()
        box = MovieHeaderBox(size, version, 0)
        if version == 0:
            box.creation_time = self.reader.read32()
            box.modification_time = self.reader.read32()
            box.timescale = self.reader.read32()
            box.duration = self.reader.read32() 
        else:
            box.creation_time = self.reader.read64()
            box.modification_time = self.reader.read64()
            box.timescale = self.reader.read32()
            box.duration = self.reader.read64()
        
        self.reader.skip(76)
        box.next_track_id = self.reader.read32()
        self.boxes['unknown'] = {}
        self.boxes['unknown']['mvhd'] = box 

    def parse_tkhd(self, size):
        version = self.reader.read8()
        flags = self.reader.readn_as_int(3)
        box = TrackHeaderBox(size, version, 0)
        if version == 0:
            box.creation_time = self.reader.read32()
            box.modification_time = self.reader.read32()
            box.track_id = self.reader.read32()
            box.reserved1 = self.reader.read32()
            box.duration = self.reader.read32()
        else:
            box.creation_time = self.reader.read64()
            box.modification_time = self.reader.read64()
            box.track_id = self.reader.read32()
            box.reserved1 = self.reader.read32()
            box.duration = self.reader.read64()

        box.reserved2.append(self.reader.read32())
        box.reserved2.append(self.reader.read32())
        box.layer = self.reader.read16()
        box.alternate_group = self.reader.read16()
        vol =  box.volume = self.reader.read16()
        #if track is audio, then set volume to 1 else 0
        #for now, set it to 0 until we figure how to check the track type
        box.volume = 0
        box.reserved3 = self.reader.read16()
        self.reader.skip(36)
        #TODO abhi - width and height values are stored as fixed point 16.16 values
        #not sure how to convert that to float at this point in time. But reading 
        #the first 16 bits and treating them as a value does the job.
        box.width = self.reader.read16()
        self.reader.skip(2)
        box.height = self.reader.read16()
        self.reader.skip(2)
        self.boxes['unknown'] = {}
        self.boxes['unknown']['tkhd'] = box 

    def parse_mdhd(self, size): 

        version = self.reader.read32()
        box = MediaHeaderBox(size, version, 0)
        if version == 0:
            box.creation_time = self.reader.read32()
            box.modification_time = self.reader.read32()
            box.timescale = self.reader.read32()
            box.duration = self.reader.read32() 
        else:
            box.creation_time = self.reader.read64()
            box.modification_time = self.reader.read64()
            box.timescale = self.reader.read32()
            box.duration = self.reader.read64()
        
        data = self.reader.readn_as_int(2)
        box.pad = (data >> 15) & 1
        language = data & 0x7fff
        box.language = chr(97 + (language >> 10) - 1 %97) + \
                       chr(97 + (language >> 5 & 0x1f) - 1 % 97) + \
                       chr(97 + (language & 0x1f) - 1 % 97)
        box.predefined = self.reader.read16()
        self.boxes['unknown'] = {}
        self.boxes['unknown']['mdhd'] = box 
 
    def get_boxes(self):
        return self.boxes
