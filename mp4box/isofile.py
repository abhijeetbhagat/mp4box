from mp4box.utils.stream_reader import StreamReader
from mp4box.box_parser import BoxParser

#This class represents both an mp4 and m4s files
class ISOFile:
    class Track:
        def __init__(self, id, user, trak):
            self.id = id
            self.user = user
            self.trak = trak
            self.segmentStream = None
            self.nb_samples = 1000
            self.samples = []

    class FragmentedTrack(Track):
        def __init__(self, id, user, trak):
            super().__init__(id, user, trak)
            self.rap_alignment = True

    class ExtractedTrack(Track):
        def __init__(self, id, user, trak):
            super().__init__(id, user, trak)

    def __init__(self, file):
        #self.stream = stream if stream else StreamReader()
        self.boxes = []
        self.mdats = []
        self.moofs = []
        self.is_progressive = False
        self.moov_start_found = False
        self.on_moov_start = None
        self.on_ready = None
        self.ready_sent = False
        self.on_segment = None
        self.on_samples = None
        self.on_error = None
        self.sample_list_built = False
        self.fragmented_tracks = []
        self.extracted_tracks = []
        self.is_fragmentation_initialized = False
        self.sample_process_started = False
        self.next_moof_number = 0
        self.item_list_built = False
        self.on_sidx = None
        self.sidx_sent = False
        self.box_parser = BoxParser(file)
        self.info = None
        self.video_trak = None
        self.audio_trak = None

    def __entry__(self):
        pass

    def __exit__(self, type, val, tb):
        pass

    def parse(self):
        self.box_parser.parse()

    def get_all_info(self):
        if self.info is None:
            self.info = self.box_parser.get_all_info()
            #TODO abhi - now, the thing is there can be multiple traks.
            #However, at the moment, we deal only with A/V traks.
            if self.info['tracks'][0].is_audio:
                self.audio_trak = self.info['tracks'][0]
                if len(self.info['tracks']) > 1:
                    self.video_trak = self.info['tracks'][1]
            else:
                self.video_trak = self.info['tracks'][0]
                if len(self.info['tracks']) > 1:
                    self.audio_trak = self.info['tracks'][1]
        return self.info

    def get_video_nalu_gen(self):
        #TODO abhi: sigh! perhaps, get_nalu_gen() can figure out the
        #video trak? but it deals only with higher level boxes like
        #ftyp, moov, mdat et. al. So for now, we have to call
        #get_all_info() which inits self.video_trak
        self.get_all_info()
        return self.box_parser.get_nalu_gen(self.video_trak)

    def frames(self, media_type):
        return self.box_parser.get_frames(media_type)
