import unittest
from tempfile import TemporaryFile
from mp4box.utils.stream_reader import StreamReader
from mp4box.parsing.ftyp import *
from mp4box.parsing.stts import *
from mp4box.parsing.stss import *
from mp4box.parsing.stsc import *

class TestTopLevelBoxes(unittest.TestCase):
    def test_ftyp(self):
         with  TemporaryFile() as f:
                f.write(b"\x00\x00\x00\x18\x66\x74\x79\x70\x69\x73\x6f\x36\x00\x00\x00\x01\x69\x73\x6f\x36\x64\x61\x73\x68")
                f.seek(0)
                reader = StreamReader(f)
                size = reader.read32()
                _ = reader.read32()
                ftyp = parse_ftyp(reader, size)
                self.assertNotEqual(ftyp, None)
                self.assertEqual(ftyp.size, 24)
                self.assertEqual(ftyp.major_brand, 'iso6')
                self.assertEqual(len(ftyp.compatible_brands), 2)
                self.assertEqual(ftyp.compatible_brands[0], 'iso6')
                self.assertEqual(ftyp.compatible_brands[1], 'dash')


class TestSampleTables(unittest.TestCase):
    def test_stts(self):
        with TemporaryFile() as f:
           f.write(b'\x00\x00\x00\x18\x73\x74\x74\x73\x00'
                   b'\x00\x00\x00\x00\x00\x00\x01\x00\x00\x02\xb0\x00\x00\x03\xe8')
           f.seek(0)
           reader = StreamReader(f)
           size = reader.read32()
           _ = reader.read32()
           stts = parse_stts(reader, size)
           self.assertNotEqual(stts, None)
           self.assertEqual(stts.entry_count, 1)
    
    def test_stss(self):
        with TemporaryFile() as f:
            f.write(b'\x00\x00\x00\x4c\x73\x74\x73\x73\x00\x00\x00\x00\x00'
                    b'\x00\x00\x0f\x00\x00\x00\x01\x00\x00\x00\x31\x00\x00'
                    b'\x00\x61\x00\x00\x00\x91\x00\x00\x00\xc1\x00\x00\x00'
                    b'\xf1\x00\x00\x01\x21\x00\x00\x01\x51\x00\x00\x01\x81'
                    b'\x00\x00\x01\xb1\x00\x00\x01\xe1\x00\x00\x02\x11\x00\x00\x02\x41'
                    b'\x00\x00\x02\x71\x00\x00\x02\xa1')
            f.seek(0)
            reader = StreamReader(f)
            size = reader.read32()
            _ = reader.read32()
            stss = parse_stss(reader, size)
            self.assertNotEqual(stss, None)

    def test_stsc(self):
        with TemporaryFile() as f:

            f.write(b'\x00\x00\x00\x34\x73\x74\x73\x63\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00'
                    b'\x00\x01\x00\x00\x00\x0d\x00\x00\x00\x01\x00\x00\x00'
                    b'\x02\x00\x00\x00\x0c\x00\x00\x00\x01\x00\x00\x00\x3a'
                    b'\x00\x00\x00\x03\x00\x00\x00\x01')
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

if __name__ == '__main__':
    test_classes_to_run = [TestTopLevelBoxes, TestSampleTables]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)