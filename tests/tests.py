"""
PymageJ Copyright (C) 2015 Jochem Smit

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License
 as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
 of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the
Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import numpy as np
import unittest
import tempfile
import os

from pymagej.roi import ROIEncoder, ROIDecoder, ROIRect, ROIFreehand, ROIOval, ROIPolygon


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

    def test_decoder_oval(self):
        with ROIDecoder('oval.roi') as roi:
            roi_obj = roi.get_roi()

        self.assertIsInstance(roi_obj, ROIOval)
        self.assertEqual(roi_obj.top, 57)
        self.assertEqual(roi_obj.left, 25)
        self.assertEqual(roi_obj.bottom, 98)
        self.assertEqual(roi_obj.right, 115)
        self.assertEqual(roi_obj.area, np.pi * (115 - 25) * (98 - 57) / 4)

    def test_decoder_polygon(self):
        with ROIDecoder('polygon.roi') as roi:
            roi_obj = roi.get_roi()

        self.assertIsInstance(roi_obj, ROIPolygon)
        self.assertEqual(roi_obj.top, 19)
        self.assertEqual(roi_obj.left, 9)
        self.assertEqual(roi_obj.bottom, 84)
        self.assertEqual(roi_obj.right, 76)
        self.assertTrue(np.allclose([0, 19, 46, 66, 20], roi_obj.x_coords))
        self.assertTrue(np.allclose([57, 22, 0, 48, 65], roi_obj.y_coords))

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

    def test_encoder_oval(self):
        roi_obj = ROIOval(100, 25, 150, 50)
        temp_path = tempfile.mkstemp()[1]
        with ROIEncoder(temp_path, roi_obj) as roi:
            roi.write()

        with ROIDecoder(temp_path) as roi:
            roi_obj = roi.get_roi()

        self.assertIsInstance(roi_obj, ROIOval)
        self.assertEqual(roi_obj.top, 100)
        self.assertEqual(roi_obj.left, 25)
        self.assertEqual(roi_obj.bottom, 150)
        self.assertEqual(roi_obj.right, 50)
        self.assertEqual(roi_obj.area, np.pi * (50 - 25) * (150 - 100) / 4)

    def test_encoder_polygon(self):
        y_coords = np.array([45, 30, 0, 12, 20])
        x_coords = np.array([0, 13, 25, 60, 5])
        left = 22
        top = 30

        right = left + np.max(x_coords) - np.min(x_coords) + 1
        bottom = top + np.max(y_coords) - np.min(y_coords) + 1

        roi_obj = ROIPolygon(top, left, bottom, right, x_coords, y_coords)
        temp_path = tempfile.mkstemp()[1]
        with ROIEncoder(temp_path, roi_obj) as roi:
            roi.write()

        with ROIDecoder(temp_path) as roi:
            roi_obj = roi.get_roi()

        self.assertIsInstance(roi_obj, ROIPolygon)
        self.assertEqual(roi_obj.top, top)
        self.assertEqual(roi_obj.left, left)
        self.assertEqual(roi_obj.bottom, bottom)
        self.assertEqual(roi_obj.right, right)
        self.assertTrue(np.allclose(x_coords, roi_obj.x_coords))
        self.assertTrue(np.allclose(y_coords, roi_obj.y_coords))


if __name__ == '__main__':
    unittest.main()