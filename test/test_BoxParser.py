import unittest
import os
from test import *
from test.context import mp4box
from mp4box.box_parser import BoxParser


class TestBoxParser(unittest.TestCase):
    def test_root_parsing(self):
        with open(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "output_squirrel.mp4"
            ),
            "rb",
        ) as f:
            bp = BoxParser(f)
            bp.parse()
            assert bp.root is not None

    def test_get_all_info(self):
        with open(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "output_squirrel.mp4"
            ),
            "rb",
        ) as f:
            bp = BoxParser(f)
            bp.parse()
            info = bp.get_all_info()
            assert info["timescale"] == 600
            assert len(info["tracks"]) == 1
            assert info["brands"][0] == "isom"
            assert not info["is_fragmented"]


if __name__ == "__main__":
    unittest.main()
