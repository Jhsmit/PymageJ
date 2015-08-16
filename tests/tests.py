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
import os
import numpy as np

from pymagej.roi import ROIEncoder, ROIDecoder, ROIRect, ROIFreehand


class MyTestCase(unittest.TestCase):
    def assertArrayEqual(self, it1, it2):
        np.testing.assert_array_equal(it1, it2)


class ROITest(MyTestCase):
    def test_decoder_freehand(self):
        with ROIDecoder('freehand.roi') as roi:
            roi_obj = roi.get_roi()
        self.assertIsInstance(roi_obj, ROIFreehand)
        self.assertEqual(len(roi_obj.x_coords), 117)
        self.assertEqual(roi_obj.name, '0272-0193')

    def test_encoder_freehand(self):
        x_coords = [1, 2, 3]
        y_coords = [4, 5, 6]
        roi_obj = ROIFreehand(20, 40, x_coords, y_coords, name='freehand_test')
        temp_path = 'temp_file.roi'

        with ROIEncoder(temp_path, roi_obj) as roi:
            roi.write()

        with ROIDecoder(temp_path) as roi:
            roi_obj_read = roi.get_roi()

        self.assertIsInstance(roi_obj_read, ROIFreehand)
        self.assertEqual(roi_obj_read.top, 20)
        self.assertEqual(roi_obj_read.left, 40)
        self.assertArrayEqual(roi_obj_read.x_coords, x_coords)
        self.assertArrayEqual(roi_obj_read.y_coords, y_coords)
        self.assertEqual(roi_obj_read.name, 'freehand_test')

        os.remove(temp_path)

    def test_decoder_rounded_rect(self):
        with ROIDecoder('rounded_rectangle.roi') as roi:
            roi_obj = roi.get_roi()

        self.assertIsInstance(roi_obj, ROIRect)
        self.assertEqual(roi_obj.top, 276)
        self.assertEqual(roi_obj.left, 145)
        self.assertEqual(roi_obj.bottom, 301)
        self.assertEqual(roi_obj.right, 191)
        self.assertAlmostEqual(roi_obj.area, 1064.15926536)
        self.assertEqual(roi_obj.name, 'rounded_rectangle')

    def test_decoder_rect(self):
        with ROIDecoder('rect.roi') as roi:
            roi_obj = roi.get_roi()
        self.assertIsInstance(roi_obj, ROIRect)
        self.assertEqual(roi_obj.top, 119)
        self.assertEqual(roi_obj.left, 136)
        self.assertEqual(roi_obj.bottom, 194)
        self.assertEqual(roi_obj.right, 247)
        self.assertEqual(roi_obj.area, 8325)
        self.assertEqual(roi_obj.name, 'rectangle')

    def test_encoder_rect(self):
        roi_obj_write = ROIRect(20, 30, 40, 50, name='test_name')
        temp_path = 'temp_file.roi'

        with ROIEncoder(temp_path, roi_obj_write) as roi:
            roi.write()

        with ROIDecoder(temp_path) as roi:
            roi_obj_read = roi.get_roi()

        self.assertIsInstance(roi_obj_read, ROIRect)
        self.assertEqual(roi_obj_read.top, 20)
        self.assertEqual(roi_obj_read.left, 30)
        self.assertEqual(roi_obj_read.bottom, 40)
        self.assertEqual(roi_obj_read.right, 50)
        self.assertEqual(roi_obj_read.area, 400)
        self.assertEqual(roi_obj_read.name, 'test_name')

        os.remove(temp_path)


if __name__ == '__main__':
    unittest.main()