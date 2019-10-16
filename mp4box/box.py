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
        self.free = None
        #in case the file is fragmented
        self.styp = None
        self.sidxs = []
        self.moofs = []
        self.mdats = []
        self.plep = None

    def has_fragments(self):
        return self.moofs

    def get_all_tracks(self):
        return self.moov.traks

    def get_duration(self):
        return self.moov.mvhd.duration

    def get_timescale(self):
        return self.moov.mvhd.timescale

    def get_compatible_brands(self):
        if self.ftyp is None: #this could be a segment file
            return self.styp.compatible_brands
        else:
            return self.ftyp.compatible_brands

    def get_creation_time(self):
        return self.moov.mvhd.creation_time

    def get_modification_time(self):
        return self.moov.mvhd.modification_time

    def has_fragments(self):
        return len(self.moofs) > 0

    #out["is_progressive"] = not sure what this means
    def has_iods(self):
        return self.moov.iods is not None

class TypeBox(Box):
    def __init__(self, size, name, major_brand: int, minor_version: int, compatible_brands: [int]):
        super().__init__(size, name)
        self.major_brand = major_brand
        self.minor_brand = minor_version
        self.compatible_brands = compatible_brands
        
class FileTypeBox(TypeBox):
    def __init__(self, size: int, major_brand: int, minor_version: int, compatible_brands: [int]):
        super().__init__(size, 'ftyp', major_brand, minor_version, compatible_brands)

class SegmentTypeBox(TypeBox):
    def __init__(self, size: int, major_brand: int, minor_version: int, compatible_brands: [int]):
        super().__init__(size, 'styp', major_brand, minor_version, compatible_brands) 

class MovieBox(Box):
    def __init__(self, size: int):
        super().__init__(size, 'moov')
        self.mvhd = None
        self.iods = None
        self.traks = []
        self.udta = None

    def get_all_tracks(self):
        return self.traks

    def has_iods(self):
        return self.iods is None

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
        self.chunk_offsets = []

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

class EditBox(Box):
    def __init__(self, size):
        super().__init__(size, 'edts')
        self.elst = None

class EditListBox(FullBox):
    def __init__(self, size, v):
        super().__init__(size, 'elst', 0, v, 0)
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
        self.smhd = None

class DataInformationBox(Box):
    def __init__(self, size):
        super().__init__(size, 'dinf')
        self.dref = None

class DataReferenceBox(FullBox):
    def __init__(self, size, v, f):
        super().__init__(size, 'dref', 0, v, f)
        self.entry_count = 0
        self.data_entries = []

class DataEntryUrlBox(FullBox):
    def __init__(self, size, v, f):
        super().__init__(size, 'url', 0, 0, f)
        self.location = None

class DataEntryUrnBox(FullBox):
    def __init__(self, size, v, f):
        super().__init__(size, 'urn', 0, 0, f)
        self.name = None
        self.location = None

class SampleTableBox(Box):
    def __init__(self, size):
        super().__init__(size, 'stbl')
        self.stsd = None
        self.stts = None
        self.ctts = None
        self.stss = None
        self.stsc = None
        self.stsz = None
        self.stco = None

    def get_samples_count(self):
        return self.stsz.sample_count

class TrackBox(Box):
    def __init__(self, size):
        super().__init__(size, 'trak')
        self.id = 0
        self.tkhd = None
        self.edts = None
        self.mdia = None
        self.udta = None
        self.is_audio = False
        self.is_video = False

    def get_stbl(self):
        #TODO abhi: should trak know about minf, stbl
        #or should it ask mdia to get it?
        return self.mdia.minf.stbl

    def get_samples_count(self):
        sample_count = 0
        stbl = self.get_stbl()
        sample_count = stbl.get_samples_count()
        return sample_count

class MediaDataBox(Box):
    def __init__(self, size, offset):
        super().__init__(size, 'mdat')
        self.offset = offset

class AVCCConfigurationBox(Box):
    def __init__(self, size):
        super().__init__(size, 'avcC')
        self.config_version = 0
        self.profile_indication = 0
        self.profile_compatibility = 0
        self.level_indication = 0
        self.len_size_minus_one = 0
        self.num_sps = 0
        self.sps_len = []
        self.sps_nalu = []
        self.num_pps = 0
        self.pps_len = []
        self.pps_nalu = []

class AVC1Box(Box):
    def __init__(self, size):
        super().__init__(size, 'avc1')
        self.data_ref_index = 0
        self.vid_enc_version = 0
        self.vid_enc_rev_lvl = 0
        self.vid_enc_vendor = 0
        self.vid_temporal_quality = 0
        self.vid_spatial_quality = 0
        self.vid_frame_pixel_size = 0
        self.vid_resolution = 0
        self.vid_data_size = 0
        self.vid_frame_count = 0
        self.vid_enc_name_len = 0
        self.vid_enc_name = ""
        self.vid_pixel_depth = 0
        self.vid_color_tbl_id = 0
        self.avcc = None
        self.btrt = None
        self.colr = None

class SampleDescriptionBox(FullBox):
    def __init__(self, size, v, f):
        super().__init__(size, 'stsd', v, 0, f)
        self.entry_count = 0
        self.avc1 = None
        self.mp4a = None

class MovieFragmentBox(Box):
    def __init__(self, size):
        super().__init__(size, 'moof')
        self.mfhd = None
        self.traf = None

class MovieFragmentHeaderBox(FullBox):
    def __init__(self, size, v, f):
        super().__init__(size, 'mfhd', 0, 0, 0)
        self.sequence_num = 0

class TrackFragmentBox(Box):
    def __init__(self, size):
        super().__init__(size, 'traf')
        self.tfhd = None
        self.tfdt = None
        self.trun = None

class TrackFragmentHeaderBox(FullBox):
    def __init__(self, size, v, f):
        super().__init__(size, 'tfhd', 0, 0, f)
        self.track_id = 0
        self.base_data_offset = 0
        self.sample_description_index = 0
        self.default_sample_duration = 0
        self.default_sample_size = 0
        self.default_sample_flag = 0

class TrackFragmentDecodingTime(FullBox):
    def __init__(self, size, v, f):
        super().__init__(size, 'tfdt', 0, v, 0)
        self.base_media_decode_time = 0

class TrackFragmentRunBox(FullBox):
    class Entry:
        def __init__(self, sample_duration, sample_size, sample_flags):
            self.sample_duration = 0
            self.sample_size = 0
            self.sample_flags = 0
            self.sample_composition_time_offset = 0

    def __init__(self, size, v, f):
        super().__init__(size, 'trun', 0, v, f)
        self.sample_count = 0
        self.data_offset = 0
        self.first_sample_flags = 0
        self.entries = []

class SegmentIndexBox(FullBox):
    class Entry:
        def __init__(self):
            self.reference_type = 0
            self.referenced_size = 0
            self.subsegment_duration = 0
            self.starts_with_SAP = 0
            self.SAP_type = 0
            self.SAP_delta_time = 0

    def __init__(self, size, v, f):
        super().__init__(size, 'sidx', 0, v, 0)
        self.ref_id = 0
        self.timescale = 0
        self.earliest_presentation_time = 0
        self.first_offset = 0
        self.reserved = 0
        self.reference_count = 0
        self.entries = []

class ColourInformationBox(Box):
    def __init__(self, size):
        super().__init__(size, 'colr')

class PixelAspectRatioBox(Box):
    def __init__(self, size):
        super().__init__(size, 'pasp')

class UserDataBox(Box):
    def __init__(self, size):
        super().__init__(size, 'udta')

class SoundMediaHeaderBox(Box):
    def __init__(self, size):
        super().__init__(size, 'smhd')

class MP4AudioBox(Box):
    def __init__(self, size):
        super().__init__(size, 'mp4a')

class PLEPBox(Box):
    def __init__(self, size):
        super().__init__(size, 'plep')
