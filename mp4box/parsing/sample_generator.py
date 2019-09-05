from mp4box.utils.sample import VideoSample

#SampleGenerator should work with both stbls and truns
#It should work with one mdat at a time.
class SampleGenerator:
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

class AudioSampleGenerator:
    def __init__(self, trak, mdat):
        pass

    def get(self):
        pass

class VideoSampleGenerator(SampleGenerator):
    def __init__(self, reader, trak, mdat):
        super().__init__(trak.get_stbl())
        self.reader = reader
        self.stbl = trak.get_stbl()
        self.mdat = mdat
    
    #TODO abhi: could this be common for audio as well?
    def get(self):
        self.reader.reset() #reset the file ptr to the beginning before we begin
        num_chunks = self.stbl.stco.entry_count
        i = 0
        for chunk_offset in self.stbl.stco.chunk_offsets:
            self.reader.skip(chunk_offset) #set the file ptr to the beginning of the chunk
            samples_per_chunk = self.get_sample_count()
            
            for _ in range(0, samples_per_chunk): 
                sample_size = self.stbl.stsz.entry_size[i]
                i += 1
                sample = VideoSample(sample_size, self.reader)
                yield sample

            #once all the samples in the current chunk are read,
            #reset the file ptr to the beginning since we skip
            #at the beginning of this loop.
            #TODO abhi: see if we can avoid this?
            self.reader.reset()

    def get_sync_sample(self, n):
        self.reader.reset() #reset the file ptr to the beginning before we begin
        j = 0
        k = 0
        for chunk_offset in self.stbl.stco.chunk_offsets:
            self.reader.skip(chunk_offset)
            samples_per_chunk = get_sample_count()
            for _ in range(0, samples_per_chunk):
                if  j == self.stbl.stss.sample_num[k]:
                    sample_size = self.stbl.stsz.entry_size[k]
                    sync_sample = VideoSample(sample_size, self.reader)
                    k += 1
                    yield sync_sample

                j += 1

            self.reader.reset()

    def get_next_sync_sample_index(self):
        stss = self.stbl.stss
        for ss in stss.sample_num:
            yield ss
