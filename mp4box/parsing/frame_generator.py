#FrameGenerator should work with both stbls and truns
#It should work with one mdat at a time.
class FrameGenerator:
    def __init__(self, stbl):
        self.stbl = stbl 

    def get_sample_count(self):
        f_o = self.stbl.stsc.first_chunk
        s_c = self.stbl.stsc.samples_per_chunk
        if self.stbl.stsc.entry_count > 1:
            i = 0
            k = 0
            while k < self.stbl.stco.entry_count:
                yield s_c[i]
                if i + 1 < self.stbl.stsc.entry_count:
                    if f_o[i+1] - (k + 1) == 1: 
                       i += 1
                    k += 1
                else:
                    break
        else:
            yield s_c[0]

class AudioFrameGenerator:
    def __init__(self, trak, mdat):
        pass

    def get(self):
        pass

class VideoFrameGenerator:
    def __init__(self, reader, trak, mdat):
        super().__init__(trak.get_stbl())
        self.reader = reader
        self.stbl = trak.get_stbl()
        self.mdat = mdat
    
    def get(self):
        self.reader.reset() #reset the file ptr to the beginning
        num_chunks = self.stbl.stco.entry_count
        for chunk_offset in self.stbl.stco.chunk_offsets:
            chunk = self.reader.readn(chunk_offset)
            samples_per_chunk = get_sample_count()
