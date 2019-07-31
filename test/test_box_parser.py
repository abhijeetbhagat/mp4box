import unittest
from tempfile import TemporaryFile
from mp4box.box_parser import BoxParser

class TestBoxParser(unittest.TestCase):
    def test_ftyp(self):
        b = 0
        with  TemporaryFile() as f:
            f.write(b"\x00\x00\x00\x18\x66\x74\x79\x70\x69\x73\x6f\x36\x00\x00\x00\x01\x69\x73\x6f\x36\x64\x61\x73\x68")
            f.seek(0)
            bp = BoxParser(f)
            bp.parse()
            boxes = bp.get_boxes()
            self.assertEqual(len(boxes.keys()), 1)

    def test_second_box_size(self):
        b = 0
        with  TemporaryFile() as f:
            f.write(b"\x00\x00\x00\x18\x66\x74\x79\x70\x69\x73\x6f\x6d\x00\x00\x00\x01\x69\x73\x6f\x6d\x61\x76\x63\x31")
            f.seek(0)
            bp = BoxParser(f)
            bp.parse()
            boxes = bp.get_boxes()
            self.assertIsNot(boxes['ftyp'], None) 

    def test_free(self):
         with  TemporaryFile() as f:

            f.write((b"\x00\x00\x00\x45\x66\x72\x65\x65\x49\x73\x6f\x4d\x65\x64\x69\x61\x20\x46\x69\x6c\x65\x20"
                     b"\x50\x72\x6f\x64\x75\x63\x65\x64\x20\x77\x69\x74\x68\x20\x47\x50\x41\x43\x20\x30\x2e\x38\x2e"
                     b"\x30\x2d\x72\x65\x76\x39\x2d\x67\x36\x65\x34\x61\x66\x30\x35\x62\x2d\x6d\x61\x73\x74\x65\x72"
                     b"\x00\x00\x00\x02\xd6"))
            f.seek(0)
            bp = BoxParser(f)
            bp.parse()
            boxes = bp.get_boxes()
            self.assertIsNot(boxes['free'], None) 

    def test_mvhd(self):
        with TemporaryFile() as f:
            f.write(b"\x00\x00\x00\x6c\x6d\x76\x68\x64\x00\x00\x00\x00\xc1\x02\x17\x10\xc1"
                    b"\x02\x17\x63\x00\x00\x02\x58\x00\x00\x4a\xb3\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                    b"\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                    b"\x00\x00\x00\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                    b"\x00\x00\x00\x00\x00\x00\x03")
            f.seek(0)
            bp = BoxParser(f)
            bp.parse()
            boxes = bp.get_boxes()
            self.assertIsNot(boxes['unknown']['mvhd'], None) 
            self.assertEqual(boxes['unknown']['mvhd'].next_track_id, 3) 

    def test_tkhd(self):
        with TemporaryFile() as f:
            f.write(b"\x00\x00\x00\x5c\x74\x6b\x68\x64\x00\x00\x00\x01\xc1\x02\x17\x13\xc1\x02\x17\x64\x00\x00\x00\x02\x00\x00\x00\x00"
                    b"\x00\x00\x49\xe8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00"
                    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x40\x00\x00\x00\x01\x40\x00\x00\x00\xf0\x00\x00")
            f.seek(0)
            bp = BoxParser(f)
            bp.parse()
            boxes = bp.get_boxes()
            self.assertNotEqual(boxes['unknown']['tkhd'], None)
            self.assertEqual(boxes['unknown']['tkhd'].duration, 18920)
            self.assertEqual(boxes['unknown']['tkhd'].width, 320)
            self.assertEqual(boxes['unknown']['tkhd'].height, 240)

if __name__ == "__main__":
    unittest.main()

