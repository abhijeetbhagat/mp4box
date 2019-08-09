import unittest
from tempfile import TemporaryFile
from mp4box.utils.stream_reader import StreamReader
from mp4box.parsing.ftyp import *

class TestBoxParsingIsolation(unittest.TestCase):
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

if __name__ == '__main__':
    unittest.main()
