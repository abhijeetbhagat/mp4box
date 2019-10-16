from mp4box.utils.nalu import NALU
from mp4box.parsing.sample_generator import VideoSampleGenerator

#SampleGenerator should work with both stbls and truns
#It should work with one mdat at a time.
class NALUGenerator:
    def __init__(self, reader, trak, mdat):
        self.vid_sample_gen = VideoSampleGenerator(reader, trak, mdat) 
        self.reader = reader

    def get_nalu(self):
        for sample in self.vid_sample_gen.get_sample():
            cnt = 0
            while cnt < sample.size:
                nalu_size = self.reader.read32()
                cnt += 4 #we just read 4 bytes
                nalu = NALU(nalu_size, self.reader) 
                cnt += nalu_size #we just read nalu_size bytes
                yield nalu

