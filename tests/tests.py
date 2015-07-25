"""
PymageJ Copyright (C) 2015 Jochem Smit

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License
 as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
 of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the
Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import unittest
import tempfile
import os

from pymagej.roi import ROIEncoder, ROIDecoder, ROIRect, ROIFreehand


class ROITest(unittest.TestCase):
    def test_decoder_freehand(self):
        with ROIDecoder('freehand.roi') as roi:
            roi_obj = roi.get_roi()
        self.assertIsInstance(roi_obj, ROIFreehand)
        self.assertEqual(len(roi_obj.x_coords), 117)

    def test_decoder_rect(self):
        with ROIDecoder('rect.roi') as roi:
            roi_obj = roi.get_roi()
        self.assertIsInstance(roi_obj, ROIRect)
        self.assertEqual(roi_obj.top, 0)
        self.assertEqual(roi_obj.left, 0)
        self.assertEqual(roi_obj.bottom, 55)
        self.assertEqual(roi_obj.right, 114)
        self.assertEqual(roi_obj.area, 6270)

    def test_encoder_rect(self):
        roi_obj = ROIRect(20, 30, 40, 50)
        temp_path = tempfile.mkstemp()[1]
        with ROIEncoder(temp_path, roi_obj) as roi:
            roi.write()

        with ROIDecoder(temp_path) as roi:
            roi_obj = roi.get_roi()

        self.assertIsInstance(roi_obj, ROIRect)
        self.assertEqual(roi_obj.top, 20)
        self.assertEqual(roi_obj.left, 30)
        self.assertEqual(roi_obj.bottom, 40)
        self.assertEqual(roi_obj.right, 50)
        self.assertEqual(roi_obj.area, 400)

        os.remove(temp_path)


if __name__ == '__main__':
    unittest.main()