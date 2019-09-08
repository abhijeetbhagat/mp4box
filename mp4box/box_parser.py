from mp4box.box import RootBox
from mp4box.parsing.ftyp import parse_ftyp
from mp4box.parsing.moov import parse_moov
from mp4box.parsing.free import parse_free
from mp4box.parsing.mdat import parse_mdat
from mp4box.utils.stream_reader import StreamReader
from mp4box.parsing.sample_generator import SampleGenerator
from mp4box.utils.exceptions import InvalidBoxError

class BoxParser:
    def __init__(self, file):
        self.reader = StreamReader(file)
        self.root = None
        self.frame_gen = None

    def parse(self):
        if not self.root:
            self.root = RootBox()
            size = self.reader.read32()
            type = self.reader.read32_as_str()
            while not self.reader.reached_eof():
                if type == 'ftyp':
                    self.root.ftyp = parse_ftyp(self.reader, size)
                elif type == 'moov':
                    self.root.moov = parse_moov(self.reader, size)
                elif type == 'free':
                    self.root.free = parse_free(self.reader, size)
                elif type == 'mdat':
                    self.root.mdats.append(parse_mdat(self.reader, size))
                else:
                    raise InvalidBoxError("type %s unknown" % type, None)
                if self.reader.reached_eof():
                    break
                #At the end of current box parsing, the file pointer will be
                #ready to read the size and type of the next box
                size = self.reader.read32()
                type = self.reader.read32_as_str()

            #Either box parsing was successful or it has errors

    def get_tree(self):
        return self.root

    def get_all_info(self):
        #TODO abhi: not sure if the metadata should be structured as a dict
        #or something else. For now, just return a dict.
        out = {}

        out["duration"] = self.root.get_duration()
        out["timescale"] = self.root.get_timescale()
        out["brands"] = self.root.get_compatible_brands()
        out["created"] = self.root.get_creation_time()
        out["modified"] = self.root.get_modification_time()
        out["tracks"] = self.root.get_all_tracks()
        out["is_fragmented"] = self.root.has_fragments()
        #out["is_progressive"] = not sure what this means
        out["has_iod"] = self.root.has_iods()

        return out

    def get_frames(self, media_type):
        #media_type can be either audio, video or both
        if not self.root:
            self.parse()

        self.frame_gen = FrameGenerator(media_type, self.root.get_all_tracks(), self.root.mdats)
        return self.frame_gen 