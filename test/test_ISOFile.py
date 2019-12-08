import os
import unittest
from tempfile import TemporaryFile
from mp4box.isofile import ISOFile


class TestISOFile(unittest.TestCase):
    def test_get_all_info(self):
        file = ISOFile(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "output_squirrel.mp4"
            )
        )
        file.parse()
        out = file.get_all_info()
        self.assertNotEqual(out, None)
        trak = out["tracks"][0]
        self.assertEqual(trak.id, 1)


if __name__ == "__main__":
    unittest.main()
