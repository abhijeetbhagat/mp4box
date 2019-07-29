import unittest

class TestBoxParsing(unittest.TestCase):
    def test_ftyp_parse(self):
        stream = b"\x00\x00\x00\x18\x66\x74\x79\x70\x69\x73\x6f\x36\x00\x00\x00\x01\x69\x73\x6f\x36\x64\x61\x73\x68"
        p = int.from_bytes(stream[0:4], "big")
        self.assertEqual(p, 24)
        #with open("C:\\Users\\gs-0834\\Downloads\\DASH_test\\output_squirrel.mp4", "rb") as f:
        #    stream = f.read(24)

if __name__ == "__main__":
    unittest.main()
