import unittest
import os
from pathlib import Path
from tempfile import TemporaryFile
from test import *
from test.context import mp4box
from mp4box.utils.stream_reader import StreamReader
from mp4box.box import FileTypeBox
from mp4box.parsing.typ import *
from mp4box.parsing.stts import *
from mp4box.parsing.stss import *
from mp4box.parsing.stsc import *
from mp4box.parsing.stco import *
from mp4box.parsing.ctts import *
from mp4box.parsing.stsz import *
from mp4box.parsing.tkhd import *
from mp4box.parsing.mvhd import *
from mp4box.parsing.mdhd import *
from mp4box.parsing.hdlr import *
from mp4box.parsing.avcc import *


class TestTopLevelBoxes(unittest.TestCase):
    def test_ftyp(self):
        with TemporaryFile() as f:
            f.write(
                b"\x00\x00\x00\x18\x66\x74\x79\x70\x69\x73\x6f\x36\x00\x00\x00\x01\x69\x73\x6f\x36\x64\x61\x73\x68"
            )
            f.seek(0)
            reader = StreamReader(f)
            size = reader.read32()
            _ = reader.read32()
            ftyp = parse_typ(reader, size, FileTypeBox)
            self.assertNotEqual(ftyp, None)
            self.assertEqual(ftyp.size, 24)
            self.assertEqual(ftyp.major_brand, "iso6")
            self.assertEqual(len(ftyp.compatible_brands), 2)
            self.assertEqual(ftyp.compatible_brands[0], "iso6")
            self.assertEqual(ftyp.compatible_brands[1], "dash")


class TestSampleTables(unittest.TestCase):
    def test_stts(self):
        with TemporaryFile() as f:
            f.write(
                b"\x00\x00\x00\x18\x73\x74\x74\x73\x00"
                b"\x00\x00\x00\x00\x00\x00\x01\x00\x00\x02\xb0\x00\x00\x03\xe8"
            )
            f.seek(0)
            reader = StreamReader(f)
            size = reader.read32()
            _ = reader.read32()
            stts = parse_stts(reader, size)
            self.assertNotEqual(stts, None)
            self.assertEqual(stts.entry_count, 1)

    def test_stss(self):
        with TemporaryFile() as f:
            f.write(
                b"\x00\x00\x00\x4c\x73\x74\x73\x73\x00\x00\x00\x00\x00"
                b"\x00\x00\x0f\x00\x00\x00\x01\x00\x00\x00\x31\x00\x00"
                b"\x00\x61\x00\x00\x00\x91\x00\x00\x00\xc1\x00\x00\x00"
                b"\xf1\x00\x00\x01\x21\x00\x00\x01\x51\x00\x00\x01\x81"
                b"\x00\x00\x01\xb1\x00\x00\x01\xe1\x00\x00\x02\x11\x00\x00\x02\x41"
                b"\x00\x00\x02\x71\x00\x00\x02\xa1"
            )
            f.seek(0)
            reader = StreamReader(f)
            size = reader.read32()
            _ = reader.read32()
            stss = parse_stss(reader, size)
            self.assertNotEqual(stss, None)

    def test_stsc(self):
        with TemporaryFile() as f:

            f.write(
                b"\x00\x00\x00\x34\x73\x74\x73\x63\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00"
                b"\x00\x01\x00\x00\x00\x0d\x00\x00\x00\x01\x00\x00\x00"
                b"\x02\x00\x00\x00\x0c\x00\x00\x00\x01\x00\x00\x00\x3a"
                b"\x00\x00\x00\x03\x00\x00\x00\x01"
            )
            f.seek(0)
            reader = StreamReader(f)
            size = reader.read32()
            _ = reader.read32()
            stsc = parse_stsc(reader, size)
            self.assertNotEqual(stsc, None)
            self.assertEqual(stsc.entry_count, 3)
            self.assertEqual(stsc.first_chunk[0], 1)
            self.assertEqual(stsc.samples_per_chunk[0], 13)
            self.assertEqual(stsc.sample_description_index[0], 1)

    def test_stco(self):
        with TemporaryFile() as f:
            f.write(
                b"\x00\x00\x00\xf8\x73\x74\x63\x6f\x00\x00\x00\x00\x00\x00\x00"
                b"\x3a\x00\x00\x23\xfb\x00\x04\xc3\x1e\x00\x05\x7b\x55\x00\x07"
                b"\x84\x5c\x00\x0a\xb0\xcd\x00\x0d\x4b\xf3\x00\x0e\x84\xa6\x00"
                b"\x0f\xf5\x77\x00\x15\x34\x84\x00\x17\x28\xb4\x00\x19\xd8\x75"
                b"\x00\x1a\xd8\x1f\x00\x1d\x4e\xdd\x00\x20\x54\xd7\x00\x22\xa4"
                b"\x7a\x00\x25\x96\x16\x00\x28\x33\x6c\x00\x29\x40\x03\x00\x2a"
                b"\xaa\x83\x00\x2b\xf2\x0f\x00\x2e\xae\xfd\x00\x30\x9f\x80\x00"
                b"\x32\xb1\xf9\x00\x34\x72\x12\x00\x37\x52\x66\x00\x39\x45\xf8"
                b"\x00\x3a\xd0\x8a\x00\x3c\xf1\x95\x00\x40\x2b\xec\x00\x42\x13"
                b"\xba\x00\x44\x1e\xbe\x00\x46\x06\x7d\x00\x49\x4a\xbd\x00\x4b"
                b"\x14\x65\x00\x4c\xf8\xd1\x00\x4f\x06\x25\x00\x52\x4c\x9a\x00"
                b"\x54\x2c\xc5\x00\x56\x6b\x81\x00\x58\xb9\xa9\x00\x5c\x23\xdb"
                b"\x00\x5d\xeb\x67\x00\x5f\x7d\x79\x00\x61\x14\x59\x00\x64\x13"
                b"\xb2\x00\x66\x20\xb7\x00\x68\x05\x1e\x00\x69\xc7\x05\x00\x6d"
                b"\x98\x41\x00\x70\x9a\xaa\x00\x72\x8c\xcd\x00\x74\xa7\x2e\x00"
                b"\x78\x88\xb8\x00\x7b\x56\x2d\x00\x7d\x6a\xc0\x00\x7f\xd0\x96"
                b"\x00\x83\x41\xdc\x00\x84\xd6\xf4"
            )
            f.seek(0)
            reader = StreamReader(f)
            size = reader.read32()
            _ = reader.read32()
            stco = parse_stco(reader, size)
            self.assertNotEqual(stco, None)
            self.assertEqual(stco.entry_count, 58)

    def test_ctts(self):
        with StreamReader(
            Path(os.path.dirname(os.path.realpath(__file__))) / "ctts_data.txt"
        ) as r:
            size = r.read32()
            _ = r.read32()
            ctts = parse_ctts(r, size)
            self.assertNotEqual(ctts, None)
            self.assertEqual(ctts.entry_count, 671)
            self.assertEqual(ctts.sample_count[0], 1)
            self.assertEqual(ctts.sample_count[1], 1)
            self.assertEqual(ctts.sample_offset[0], 2000)
            self.assertEqual(ctts.sample_offset[1], 5000)

    def test_stsz(self):
        with StreamReader(
            Path(os.path.dirname(os.path.realpath(__file__))) / "stsz_data.txt"
        ) as r:
            size = r.read32()
            _ = r.read32()
            stsz = parse_stsz(r, size)
            self.assertNotEqual(stsz, None)
            self.assertEqual(stsz.sample_size, 0)
            self.assertEqual(stsz.sample_count, 688)
            self.assertEqual(stsz.entry_size[0], 160959)
            self.assertEqual(stsz.entry_size[687], 8073)


class TestTraks(unittest.TestCase):
    def test_video_tkhd(self):
        with TemporaryFile() as f:
            f.write(
                b"\x00\x00\x00\x5c\x74\x6b\x68\x64\x00\x00\x00\x01\xc1\x02\x17\x13\xc1\x02\x17\x64\x00\x00\x00\x02\x00\x00\x00\x00"
                b"\x00\x00\x49\xe8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00"
                b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00"
                b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x40\x00\x00\x00\x01\x40\x00\x00\x00\xf0\x00\x00"
            )
            f.seek(0)
            with StreamReader(f) as reader:
                size = reader.read32()
                _ = reader.read32()
                tkhd = parse_tkhd(reader, size)
                self.assertNotEqual(tkhd, None)
                self.assertEqual(tkhd.duration, 18920)
                self.assertEqual(tkhd.width, 320)
                self.assertEqual(tkhd.height, 240)


class TestMoov(unittest.TestCase):
    def test_mvhd(self):
        with TemporaryFile() as f:
            f.write(
                b"\x00\x00\x00\x6c\x6d\x76\x68\x64\x00\x00\x00\x00\xc1\x02\x17\x10\xc1"
                b"\x02\x17\x63\x00\x00\x02\x58\x00\x00\x4a\xb3\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                b"\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                b"\x00\x00\x00\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                b"\x00\x00\x00\x00\x00\x00\x03"
            )
            f.seek(0)
            with StreamReader(f) as reader:
                size = reader.read32()
                _ = reader.read32()
                mvhd = parse_mvhd(reader, size)
                self.assertIsNot(mvhd, None)
                self.assertEqual(mvhd.next_track_id, 3)


class TestMdia(unittest.TestCase):
    def test_video_mdhd(self):
        with TemporaryFile() as f:
            f.write(
                b"\x00\x00\x00\x20\x6d\x64\x68\x64\x00\x00\x00"
                b"\x00\xc1\x02\x17\x13\xc1\x02\x17\x64\x00\x00\x00\x0f\x00\x00\x01\xd9\x15\xc7\x00\x00"
            )
            f.seek(0)
            with StreamReader(f) as reader:
                size = reader.read32()
                _ = reader.read32()
                mdhd = parse_mdhd(reader, size)
                self.assertNotEqual(mdhd, None)
                self.assertEqual(mdhd.timescale, 15)
                self.assertEqual(mdhd.duration, 473)
                self.assertEqual(mdhd.pad, 0)
                self.assertEqual(mdhd.language, "eng")

    def test_video_hdlr(self):
        with TemporaryFile() as f:
            f.write(
                b"\x00\x00\x00\x44\x68\x64\x6c\x72\x00\x00\x00\x00\x00\x00"
                b"\x00\x00\x76\x69\x64\x65\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x32\x36\x34"
                b"\x40\x47\x50\x41\x43\x30\x2e\x38\x2e\x30\x2d\x72\x65\x76\x39\x2d\x67\x36"
                b"\x65\x34\x61\x66\x30\x35\x62\x2d\x6d\x61\x73\x74\x65\x72\x00"
            )
            f.seek(0)
            with StreamReader(f) as reader:
                size = reader.read32()
                _ = reader.read32()
                hdlr = parse_hdlr(reader, size)
                self.assertNotEqual(hdlr, None)
                self.assertEqual(hdlr.handler_type, "vide")
                self.assertEqual(hdlr.name, "264@GPAC0.8.0-rev9-g6e4af05b-master\x00")


class TestAVC(unittest.TestCase):
    def test_avcc(self):
        with TemporaryFile() as f:
            f.write(
                b"\x00\x00\x00\x2f\x61\x76\x63\x43\x01\x42\xe0\x15\xff\xe1\x00\x18\x27"
                b"\x42\xe0\x15\xa9\x18\x3c\x11\xfd\x60\x2d\x41\x80\x41\xad\xb7\xa0\x0f"
                b"\x48\x0f\x55\xef\x7c\x04\x01\x00\x04\x28\xde\x09\x88"
            )
            f.seek(0)
            with StreamReader(f) as reader:
                size = reader.read32()
                _ = reader.read32()
                avcc = parse_avcc(reader, size)
                self.assertNotEqual(avcc, None)
                self.assertEqual(avcc.config_version, 1)
                self.assertEqual(avcc.level_indication, 21)
                self.assertEqual(avcc.len_size_minus_one, 3)
                self.assertEqual(avcc.num_sps, 1)
                self.assertEqual(avcc.num_pps, 1)
                self.assertEqual(avcc.sps_len, [24])
                self.assertEqual(avcc.pps_len, [4])


if __name__ == "__main__":
    test_classes_to_run = [
        TestTopLevelBoxes,
        TestSampleTables,
        TestTraks,
        TestMoov,
        TestMdia,
        TestAVC,
    ]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)
    sys.exit(not results.wasSuccessful())
