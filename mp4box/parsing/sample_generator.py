from mp4box.utils.sample import VideoSample
from mp4box.utils.stream_reader import StreamReader

# SampleGenerator should work with both stbls and truns
# It should work with one mdat at a time.
class SampleGenerator:
    def __init__(self, stbl):
        self.stbl = stbl

    def get_sample_count(self):
        f_o = self.stbl.stsc.first_chunk
        s_c = self.stbl.stsc.samples_per_chunk
        lim = self.stbl.stsz.sample_count
        k = 0
        if self.stbl.stsc.entry_count > 1:
            i = 0
            j = i + 1
            op1 = f_o[j]
            op2 = f_o[i]
            c = 0
            # stsz table tells the total count of samples
            while k < lim:
                d = op1 - op2
                v = s_c[c]

                if d == 1:
                    i += 1
                    j += 1
                    if j >= len(f_o):
                        op1 = lim
                        c = len(s_c) - 1
                    else:
                        op2 = f_o[i]
                        op1 = f_o[j]
                        c += 1
                else:
                    op2 += 1
                yield v
                k += 1
        else:
            # TODO abhi: fix me - we have the same loop above
            while k < lim:
                yield s_c[0]
                k += 1


class AudioSampleGenerator:
    def __init__(self, trak, mdat):
        pass

    def get(self):
        pass


class VideoSampleGenerator(SampleGenerator):
    def __init__(self, reader: StreamReader, trak, mdat):
        super().__init__(trak.get_stbl())
        self.reader = reader
        self.stbl = trak.get_stbl()
        self.mdat = mdat

    # TODO abhi: could this be common for audio as well?
    def get_sample(self):
        self.reader.reset()  # reset the file ptr to the beginning before we begin
        num_chunks = self.stbl.stco.entry_count
        i = 0
        samples_per_chunk = self.get_sample_count()
        for chunk_offset in self.stbl.stco.chunk_offsets:
            self.reader.skip(
                chunk_offset
            )  # set the file ptr to the beginning of the chunk

            lim = next(samples_per_chunk)
            for _ in range(0, lim):
                sample_size = self.stbl.stsz.entry_size[i]
                i += 1
                sample = VideoSample(sample_size, self.reader)
                yield sample

            # once all the samples in the current chunk are read,
            # reset the file ptr to the beginning since we skip
            # at the beginning of this loop.
            # TODO abhi: see if we can avoid this?
            self.reader.reset()

    def get_sample_sizes(self):
        i = 0
        samples_per_chunk = self.get_sample_count()
        for chunk_offset in self.stbl.stco.chunk_offsets:
            self.reader.skip(
                chunk_offset
            )  # set the file ptr to the beginning of the chunk
            lim = next(samples_per_chunk)
            for _ in range(0, lim):
                sample_size = self.stbl.stsz.entry_size[i]
                i += 1
                yield sample_size

    def get_generator_pos(self):
        return self.reader.current_pos()

    def get_sync_sample(self, n):
        self.reader.reset()  # reset the file ptr to the beginning before we begin
        j = 0
        k = 0
        for chunk_offset in self.stbl.stco.chunk_offsets:
            self.reader.skip(chunk_offset)
            samples_per_chunk = self.get_sample_count()
            for _ in range(0, samples_per_chunk):
                if j == self.stbl.stss.sample_num[k]:
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
