import unittest
import os
import itertools
from test import *
from test.context import mp4box
from mp4box.utils.stream_reader import StreamReader
from mp4box.parsing.nalu_generator import NALUGenerator
from mp4box.isofile import ISOFile

class TestNALUGeneration(unittest.TestCase):
    def test_sample_count_generation(self):
        iso_file = ISOFile(os.path.join(os.path.dirname(os.path.realpath(__file__)), "output_squirrel.mp4"))
        iso_file.parse()
        top5_nals = list(itertools.islice(iso_file.get_video_nalu_gen().get_nalu(), 5))
        self.assertEqual(top5_nals[0].size, 751)
        self.assertEqual(top5_nals[1].size, 160200)
        self.assertEqual(top5_nals[2].size, 68102)
        self.assertEqual(top5_nals[3].size, 9498)
        self.assertEqual(top5_nals[4].size, 5513)

    @unittest.skip("This is to test the decoding algo")
    def test_rle_decoding(self):
        a = [1, 2, 58]
        b = [13, 12, 3]
        k = 0
        i = 0
        j = i + 1
        op1 = a[j]
        op2 = a[i]
        c = 0
        while k < 688:
            d = op1 - op2
            v = b[c]
           
            if d == 1:
                i += 1
                j += 1
                if j >= len(a):
                    op1 = 688
                    c = len(b) - 1
                else:
                    op2 = a[i]
                    op1 = a[j]
                    c += 1
            else:
                op2 += 1
            print(v)
            k += 1

if __name__ == "__main__":
    unittest.main()
