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
        def __init__(self, id, user, track):
            super().__init__(id, user, trak)

    def __init__(self, stream):
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

    def __entry__(self):
        pass

    def __exit__(self, type, val, tb):
        pass

    def set_segment_options(self, id, user, options):
        trak = self.get_track_id(id)
        if trak:
            trak.next_sample = 0
            frag_trak = ISOFile.FragmentedTrack(id, user, trak)
            self.fragmented_tracks.append(frag_trak)
            if options:
                if options.nb_subsamples:
                    frag_trak.nb_samples = options.nb_samples 
                if options.rap_alignment:
                    frag_trak.rap_alignement = options.rap_alignment 

    def unset_segment_options(self, id):
        index = -1
        for i in range(len(self.fragmented_tracks)):
            frag_trak = self.fragmented_tracks[i]
            if frag_trak.id is id:
                index = i
                break
        self.fragmented_tracks.pop(index)

    def set_extraction_options(self, id, user, options):
        trak = self.get_track_id(id)
        if trak:
            trak.next_sample = 0
            extracted_trak = ISOFile.ExtractedTrack(id, user, trak)
            self.extracted_tracks.append(extracted_track)
            if options:
                if options.nb_subsamples:
                    extracted_trak.nb_samples = options.nb_samples 

    def unset_extraction_options(self, id):
        index = -1
        for i in range(len(self.extracted_tracks)):
            extracted_trak = self.extracted_tracks[i]
            if extracted_trak.id is id:
                index = i
                break
        self.extracted_tracks.pop(index)

    def parse(self):
        self.box_parser.parse()

    def frames(self, media_type):
        return self.box_parser.get_frames(media_type)
