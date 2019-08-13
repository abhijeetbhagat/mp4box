class Box:
    def __init__(self, size: int, box_type: str, uuid = 0):
        self.size = size
        self.type = box_type
        self.uuid = uuid

class FullBox(Box):
    def __init__(self, size: int, box_type: str, uuid, v: int, f: int):
        super().__init__(size, box_type, uuid)
        #Boxes with an unrecognized version shall be ignored and skipped. 
        self.version = v
        self.flags = f

class RootBox():
    def __init__(self):
        self.ftyp = None
        self.moov = None
        self.mdat = None
        self.free = None

class FileTypeBox(Box):
    def __init__(self, size: int, major_brand: int, minor_version: int, compatible_brands: [int]):
        super().__init__(size, 'ftyp')
        self.major_brand = major_brand
        self.minor_brand = minor_version
        self.compatible_brands = compatible_brands

class MovieBox(Box):
    def __init__(self, size: int):
        super().__init__(size, 'moov')
        self.mvhd = None
        self.iods = None
        self.trak = None

class MovieHeaderBox(FullBox):
    def __init__(self, size: int, v: int, f: int):
        super().__init__(size, 'mvhd', 0, v, f)
        self.creation_time = 0
        self.modification_time = 0
        self.timescale = 0
        self.duration = 0
        self.rate = 0x00010000
        self.volume = 0x0100
        self.reserved = 0
        self.matrix = [0x00010000,0,0,0,0x00010000,0,0,0,0x40000000]
        self.predefined = []
        self.next_track_id = 0

class FreeSpaceBox(Box):
    def __init__(self, size: int, data: [int]):
        super().__init__(size, 'free')
        #TODO abhi: this probably contains printable chars? How do we treat
        #this array of bytes
        self.data = data

class TrackHeaderBox(FullBox):
    def __init__(self, size: int, v: int, f: int):
        super().__init__(size, 'tkhd', 0, v, f)
        self.creation_time = 0
        self.modification_time = 0
        self.track_id = 0
        self.reserved1 = 0
        self.duration = 0
        self.reserved2 = []
        self.layer = 0
        self.alternate_group = 0
        self.volume = 0
        self.reserved3 = 0
        self.matrix = [0x00010000,0,0,0,0x00010000,0,0,0,0x40000000]
        self.width = 0.0
        self.height = 0.0

class MediaHeaderBox(FullBox):
    def __init__(self, size: int, v: int, f: int):
        super().__init__(size, 'mdhd', 0, v, f)
        self.creation_time = 0
        self.modification_time = 0
        self.timescale = 0
        self.duration = 0
        self.pad = 0
        self.language = ''

class TimeToSampleBox(FullBox):
    def __init__(self, size, v, f):
        super().__init__(size, 'stts', 0, v, f)
        self.entry_count = 0
        self.sample_count = []
        self.sample_delta = []

class SyncSampleBox(FullBox):
    def __init__(self, size, v, f):
        super().__init__(size, 'stss', 0, v, f)
        self.entry_count = 0
        self.sample_number = []

class SampleToChunkBox(FullBox):
    def __init__(self, size, v, f):
        super().__init__(size, 'stsc', 0, v, f)
        self.entry_count = 0
        self.first_chunk = []
        self.samples_per_chunk = []
        self.sample_description_index = []
 
class SampleSizeBox(FullBox):
    def __init__(self, size, v, f):
        super().__init__(size, 'stsz', 0, v, f)
        self.sample_size = 0
        self.sample_count = 0
        self.entry_size = []

class CompositionTimeToSampleBox(FullBox):
    def __init__(self, size, v, f):
        super().__init__(size, 'ctts', 0, v, f)
        self.sample_count = []
        self.sample_offset = []

class ChunkOffsetBox(FullBox):
    def __init__(self, size, v, f):
        super().__init__(size, 'stco', 0, v, f)
        self.entry_count = 0
        self.chunk_offset = []

class BitRateBox(Box):
    def __init__(self, size):
        super().__init__(size, 'btrt')
        self.buffer_size_db = 0
        self.max_bitrate = 0
        self.avg_bitrate = 0

class HandlerBox(FullBox):
    def __init__(self, size, v, f):
        super().__init__(size, 'hdlr', 0, v, f)
        self.predefined = 0
        self.handler_type = 0
        self.reserved = []
        self.name = ''

class EditListBox(FullBox):
    def __init__(self, size, v, f):
        super().__init__(size, 'elst', 0, v, f)
        self.entry_count = 0
        self.segment_duration = []
        self.media_time = []
        self.media_rate_integer = []
        self.media_rate_fraction = []

class VideoMediaHeaderBox(FullBox):
    def __init__(self, size, v, f):
        super().__init__(size, 'vmhd', 0, v, f)
        self.graphics_mode = 0
        self.opcolor = []

class MediaBox(Box):
    def __init__(self, size):
        super().__init__(size, 'mdia')
        self.mdhd = None
        self.hdlr = None
        self.minf = None

class MediaInformationBox(Box):
    def __init__(self, size):
        super().__init__(size, 'minf')
        self.vmhd = None
        self.dinf = None
        self.stbl = None

class DataInformationBox(Box):
    def __init__(self, size):
        super().__init__(size, 'dinf')
        self.dref = None

class DataReferenceBox(FullBox):
    def __init__(self, size, v, f):
        super().__init__(size, 'dref', 0, v, f)
        self.url = None

class SampleTableBox(Box):
    def __init__(self, size, v, f):
        super().__init__(size, 'stbl')
        self.stsd = None
        self.stts = None
        self.ctts = None
        self.stss = None
        self.stsc = None
        self.stsz = None
        self.stco = None

class TrackBox(Box):
    def __init__(self, size):
        super().__init__(size, 'trak')
        self.tkhd = None
        self.edts = None
        self.mdia = None

class MediaDataBox(Box):
    def __init__(self, size, offset):
        super().__init__(size, 'mdat')
        #this is not set to 0 because mdat can be the first box in the file?
        self.offset = -1

class RootBox:
    def __init__(self):
        self.ftyp = None
        self.moov = None
        self.mdat = None
        self.free = None
