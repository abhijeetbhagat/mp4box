import unittest
from test import *
from test.context import mp4box
from mp4box.parsing.sample_generator import SampleGenerator
from mp4box.parsing.sample_generator import VideoSampleGenerator
from mp4box.utils.stream_reader import StreamReader
from mp4box.box import SampleTableBox
from mp4box.box import SampleToChunkBox
from mp4box.box import SampleSizeBox
from mp4box.box import ChunkOffsetBox
from mp4box.box import SyncSampleBox


class TestSampleGeneration(unittest.TestCase):
    def test_sample_count_generation(self):
        stbl = SampleTableBox(0)
        stbl.stsc = SampleToChunkBox(0, 0, 0)
        stbl.stco = ChunkOffsetBox(0, 0, 0)
        stbl.stco.entry_count = 3
        stbl.stsc.entry_count = 3
        stbl.stsc.first_chunk = [1, 2, 3]
        stbl.stsc.samples_per_chunk = [1, 1, 1]
        stbl.stsz = SampleSizeBox(0, 0, 0)
        stbl.stsz.sample_count = 3
        fg = SampleGenerator(stbl)
        g = fg.get_sample_count()
        self.assertEqual(next(g), 1)
        self.assertEqual(next(g), 1)
        self.assertEqual(next(g), 1)

    def test_sample_count_generation_2(self):
        stbl = SampleTableBox(0)
        stbl.stsc = SampleToChunkBox(0, 0, 0)
        stbl.stco = ChunkOffsetBox(0, 0, 0)
        stbl.stco.entry_count = 3
        stbl.stsc.entry_count = 3
        stbl.stsc.first_chunk = [1, 2, 3]
        stbl.stsc.samples_per_chunk = [6, 7, 8]
        stbl.stsz = SampleSizeBox(0, 0, 0)
        stbl.stsz.sample_count = 3
        fg = SampleGenerator(stbl)
        g = fg.get_sample_count()
        self.assertEqual(next(g), 6)
        self.assertEqual(next(g), 7)
        self.assertEqual(next(g), 8)

    def test_sample_count_generation_3(self):
        stbl = SampleTableBox(0)
        stbl.stsc = SampleToChunkBox(0, 0, 0)
        stbl.stco = ChunkOffsetBox(0, 0, 0)
        stbl.stco.entry_count = 8
        stbl.stsc.entry_count = 3
        stbl.stsc.first_chunk = [1, 2, 8]
        stbl.stsc.samples_per_chunk = [1, 2, 3]
        stbl.stsz = SampleSizeBox(0, 0, 0)
        stbl.stsz.sample_count = 8
        fg = SampleGenerator(stbl)
        g = fg.get_sample_count()
        self.assertEqual(next(g), 1)
        self.assertEqual(next(g), 2)
        self.assertEqual(next(g), 2)
        self.assertEqual(next(g), 2)
        self.assertEqual(next(g), 2)
        self.assertEqual(next(g), 2)
        self.assertEqual(next(g), 2)
        self.assertEqual(next(g), 3)
        self.assertRaises(StopIteration, next, g)

    def test_sample_count_generation_4(self):
        stbl = SampleTableBox(0)
        stbl.stsc = SampleToChunkBox(0, 0, 0)
        stbl.stco = ChunkOffsetBox(0, 0, 0)
        stbl.stco.entry_count = 1
        stbl.stsc.entry_count = 1
        stbl.stsc.first_chunk = [1]
        stbl.stsc.samples_per_chunk = [1]
        stbl.stsz = SampleSizeBox(0, 0, 0)
        stbl.stsz.sample_count = 1
        fg = SampleGenerator(stbl)
        g = fg.get_sample_count()
        self.assertEqual(next(g), 1)
        self.assertRaises(StopIteration, next, g)

    @unittest.skip("Do not test until integration tests are done")
    def test_video_sample_generation(self):
        stbl = SampleTableBox(0)
        stbl.stsc = SampleToChunkBox(0, 0, 0)
        stbl.stco = ChunkOffsetBox(0, 0, 0)
        stbl.stco.entry_count = 1
        stbl.stsc.entry_count = 1
        stbl.stsc.first_chunk = [1]
        stbl.stsc.samples_per_chunk = [1]
        with open("output_squirrel.mp4") as f:
            reader = StreamReader(f)
            parse_trak(reader, size)
            fg = VideoSampleGenerator(reader, stbl)

    @unittest.skip("Do not test until integration tests are done")
    def test_sync_sample(self):
        stbl = SampleTableBox(0, 0, 0)
        stbl.stsc = SampleToChunkBox(0, 0, 0)
        stbl.stco = ChunkOffsetBox(0, 0, 0)
        stbl.stco.entry_count = 4
        stbl.stsc.entry_count = 3
        stbl.stsc.first_chunk = [1, 2, 58]
        stbl.stsc.samples_per_chunk = [13, 12, 3]
        stbl.stss = SyncSampleBox(0, 0, 0)
        stbl.stss.entry_count = 4
        stbl.stss.sample_number = [1, 49, 97]


if __name__ == "__main__":
    unittest.main()
