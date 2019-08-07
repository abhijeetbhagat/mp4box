from mp4box.box import FileTypeBox
from mp4box.box import MovieBox
from mp4box.box import FreeSpaceBox
from mp4box.box import MovieHeaderBox
from mp4box.box import TrackHeaderBox
from mp4box.box import MediaHeaderBox
from mp4box.box import TimeToSampleBox
from mp4box.box import SyncSampleBox
from mp4box.box import SampleToChunkBox
from mp4box.box import SampleSizeBox
from mp4box.box import ChunkOffsetBox
from mp4box.box import BitRateBox
from mp4box.box import HandlerBox
from mp4box.box import EditListBox
from mp4box.box import VideoMediaHeaderBox
from mp4box.utils.stream_reader import StreamReader
from mp4box.utils.exceptions import InvalidBoxError

class BoxParser:
    def __init__(self, file):
        self.reader = StreamReader(file)
        #TODO abhi: should this be a dict or a RootBox type?
        self.boxes = {}

    def parse(self):
        size = self.reader.read32()
        type = self.reader.read32_as_str()
        while True:
            if type == 'ftyp':
                self.parse_ftyp(size)
            elif type == 'moov':
                self.parse_moov(size)
            elif type == 'free':
                self.parse_free(size)
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

    def parse_ftyp(self, my_size):
        major_brand = self.reader.read32_as_str()
        minor_version = self.reader.read32()
        compatible_brands = []
        cnt = 0
        while cnt < my_size + 4 - 16 - 4:
            compatible_brands.append(self.reader.read32_as_str())
            cnt += 4
        box = FileTypeBox(my_size, major_brand, minor_version, compatible_brands)
        self.boxes['ftyp'] = box

    def parse_moov(self, my_size):
        box = MovieBox(my_size)
        cnt = 0
        while not self.reader.reached_eof() and cnt < my_size:
            size = self.reader.read32()
            type = self.reader.read32()
            cnt += size
            if type is 'mvhd':
                parse_mvhd(self, size)
            elif type is 'trak': 
                parse_trak(self, size)
            elif type is 'iods': 
                raise NotImplementedError
            else:
                raise InvalidBoxError("type %s unknown" % type, None)

        self.boxes['moov'] = box

    def parse_trak(self, my_size):
        size = self.reader.read32()
        type = self.reader.read32()
        cnt = 0
        while cnt < my_size:
            if type is 'tkhd':
                parse_tkhd()
            elif type is 'edts':
                parse_edts()
            elif type is 'mdia':
                parse_mdia()
            else:
                raise InvalidBoxError("type %s unknown")

    def parse_elst(self, size):
        version = self.reader.read32()
        box = EditListBox(size, version) 
        entry_count = self.reader.read32()
        for _ in range(0..entry_count):
            if version == 1:
                box.segment_duration.append(self.reader.read64())
                box.media_time.append(self.reader.read64())
            else:
                box.segment_duration.append(self.reader.read32())
                box.media_time.append(self.reader.read32()) 

            box.media_rate_integer.append(self.reader16())
            box.media_rate_fraction.append(self.reader16())
        
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

    def parse_stts(self, size):
        entry_count = self.reader.read32()
        box = TimeToSampleBox(size, 0, 0)
        box.entry_count = entry_count
        for _ in range(0, entry_count):
            box.sample_count.append(self.reader.read32())
            box.sample_delta.append(self.reader.read32())

    def parse_stss(self, size):
        entry_count = self.reader.read32()
        box = SyncSampleBox(size, 0, 0)
        box.entry_count = entry_count
        for _ in range(0, entry_count):
            box.sample_number.append(self.reader.read32())

    def parse_stsc(self, size):
        entry_count = self.reader.read32()
        box = SampleToChunkBox(size, 0, 0)
        box.entry_count = entry_count
        for _ in range(0, entry_count):
            box.first_chunk.append(self.reader.read32())
            box.samples_per_chunk.append(self.reader.read32())
            box.sample_description_index.append(self.reader.read32())
 
    def parse_stsz(self, size):
        box = SampleSizeBox(size, 0, 0)
        box.sample_size = self.reader.read32()
        box.sample_count = self.reader.read32()
        if box.sample_size:
            for _ in range(0, box.sample_count):
                box.entry_size.append(self.reader.read32())

    def parse_stco(self, size):
        box = ChunkOffsetBox(size, 0, 0)
        box.entry_count = self.reader.read32()
        for _ in range(0, box.entry_count):
            box.chunk_offset.append(self.reader.read32())

    def parse_btrt(self, size):
        box = BitRateBox(size)
        box.buffer_size_db = self.reader.read32()
        box.max_bitrate = self.reader.read32()
        box.avg_bitrate = self.reader.read32()

    def parse_hdlr(self, size):
        version = self.reader.read32()
        box = HandlerBox(size, version, 0)
        box.predefined = self.reader.read32()
        box.handler_type = self.reader.read32_as_str()
        box.reserved.append(self.reader.read32())
        box.reserved.append(self.reader.read32())
        box.reserved.append(self.reader.read32())
        box.name = self.reader.readn_as_str(size - 32)
        self.boxes['unknown'] = {}
        self.boxes['unknown']['hdlr'] = box 

    def parse_vmhd(self, size):
        self.reader.read32()
        box = VideoMediaHeaderBox(size, 0, 1)
        box.graphics_mode = self.reader.reader16()
        box.opcolor.append(self.reader.reader16())
        box.opcolor.append(self.reader.reader16())
        box.opcolor.append(self.reader.reader16()) 
        
    def get_boxes(self):
        return self.boxes
