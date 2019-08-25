import unittest
from test import *
from context import mp4box
from mp4box.parsing.ftyp import *
from mp4box.parsing.frame_generator import FrameGenerator
from mp4box.box import SampleTableBox
from mp4box.box import SampleToChunkBox
from mp4box.box import ChunkOffsetBox

class TestFrameGeneration(unittest.TestCase):
    def test_sample_count_generation(self):
        stbl = SampleTableBox(0,0,0)
        stbl.stsc = SampleToChunkBox(0,0,0)
        stbl.stco = ChunkOffsetBox(0,0,0)
        stbl.stco.entry_count = 3
        stbl.stsc.entry_count = 3
        stbl.stsc.first_chunk = [1,2,3]
        stbl.stsc.samples_per_chunk = [1,1,1]
        fg = FrameGenerator(stbl)
        g = fg.get_sample_count()
        self.assertEqual(next(g), 1)
        self.assertEqual(next(g), 1)
        self.assertEqual(next(g), 1)

    def test_sample_count_generation_2(self):
        stbl = SampleTableBox(0,0,0)
        stbl.stsc = SampleToChunkBox(0,0,0)
        stbl.stco = ChunkOffsetBox(0,0,0)
        stbl.stco.entry_count = 3
        stbl.stsc.entry_count = 3
        stbl.stsc.first_chunk = [1,2,3]
        stbl.stsc.samples_per_chunk = [6,7,8]
        fg = FrameGenerator(stbl)
        g = fg.get_sample_count()
        self.assertEqual(next(g), 6)
        self.assertEqual(next(g), 7)
        self.assertEqual(next(g), 8)

    def test_sample_count_generation_3(self):
        stbl = SampleTableBox(0,0,0)
        stbl.stsc = SampleToChunkBox(0,0,0)
        stbl.stco = ChunkOffsetBox(0,0,0)
        stbl.stco.entry_count = 8
        stbl.stsc.entry_count = 3
        stbl.stsc.first_chunk = [1,2,8]
        stbl.stsc.samples_per_chunk = [1,2,3]
        fg = FrameGenerator(stbl)
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
        stbl = SampleTableBox(0,0,0)
        stbl.stsc = SampleToChunkBox(0,0,0)
        stbl.stco = ChunkOffsetBox(0,0,0)
        stbl.stco.entry_count = 1
        stbl.stsc.entry_count = 1
        stbl.stsc.first_chunk = [1]
        stbl.stsc.samples_per_chunk = [1]
        fg = FrameGenerator(stbl)
        g = fg.get_sample_count()
        self.assertEqual(next(g), 1)
        self.assertRaises(StopIteration, next, g)

if __name__ == "__main__":
    unittest.main()
