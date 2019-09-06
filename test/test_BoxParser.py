import unittest
import os
from test import *
from context import mp4box
from mp4box.box_parser import BoxParser

class TestBoxParser(unittest.TestCase):
    def test_root_parsing(self):
        with open(os.path.dirname(os.path.realpath(__file__)) + "\output_squirrel.mp4", "rb") as f:
            bp = BoxParser(f)
            bp.parse()
            assert(bp.root is not None)

if __name__ == "__main__":
    unittest.main()

