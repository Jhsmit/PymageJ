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

from pymagej.roi import ROIEncoder, ROIDecoder, ROIRect, ROIFreehand, ROIOval, ROIPolygon, ROILine, ROIPolyline

directory = os.path.dirname(__file__)


class ROITest(unittest.TestCase):
    def test_decoder_freehand(self):
        with ROIDecoder(os.path.join(directory, 'freehand.roi')) as roi:
            roi_obj = roi.get_roi()
        self.assertIsInstance(roi_obj, ROIFreehand)
        self.assertEqual(len(roi_obj.x_coords), 117)

    def test_encoder_freehand(self):
        x_coords = np.array([1, 2, 3, 10, 15])
        y_coords = np.array([4, 5, 6, 8, 20])
        roi_obj = ROIFreehand(20, 40, 20 + x_coords.max(), 40 + y_coords.max(), x_coords, y_coords, name='freehand_test')
        temp_path = tempfile.mkstemp()[1]

        with ROIEncoder(temp_path, roi_obj) as roi:
            roi.write()

        with ROIDecoder(temp_path) as roi:
            roi_obj_read = roi.get_roi()

        self.assertIsInstance(roi_obj_read, ROIFreehand)
        self.assertEqual(roi_obj_read.top, 20)
        self.assertEqual(roi_obj_read.left, 40)
        self.assertTrue(np.allclose(roi_obj_read.x_coords, x_coords))
        self.assertTrue(np.allclose(roi_obj_read.y_coords, y_coords))
        self.assertEqual(roi_obj_read.name, 'freehand_test')

    def test_decoder_rect(self):
        with ROIDecoder(os.path.join(directory, 'rect.roi')) as roi:
            roi_obj = roi.get_roi()
        self.assertIsInstance(roi_obj, ROIRect)
        self.assertEqual(roi_obj.top, 0)
        self.assertEqual(roi_obj.left, 0)
        self.assertEqual(roi_obj.bottom, 55)
        self.assertEqual(roi_obj.right, 114)
        self.assertEqual(roi_obj.area, 6270)

    def test_encoder_rect(self):
        roi_obj = ROIRect(20, 30, 40, 50, name='rect_test')
        temp_path = tempfile.mkstemp()[1]
        with ROIEncoder(temp_path, roi_obj) as roi:
            roi.write()

        with ROIDecoder(temp_path) as roi:
            roi_out = roi.get_roi()

        self.assertIsInstance(roi_out, ROIRect)
        self.assertEqual(roi_out.top, 20)
        self.assertEqual(roi_out.left, 30)
        self.assertEqual(roi_out.bottom, 40)
        self.assertEqual(roi_out.right, 50)
        self.assertEqual(roi_out.area, 400)
        self.assertEqual(roi_out.name, 'rect_test')

    def test_decoder_oval(self):
        with ROIDecoder(os.path.join(directory, 'oval.roi')) as roi:
            roi_obj = roi.get_roi()

        self.assertIsInstance(roi_obj, ROIOval)
        self.assertEqual(roi_obj.top, 57)
        self.assertEqual(roi_obj.left, 25)
        self.assertEqual(roi_obj.bottom, 98)
        self.assertEqual(roi_obj.right, 115)
        self.assertEqual(roi_obj.area, np.pi * (115 - 25) * (98 - 57) / 4)

    def test_encoder_oval(self):
        roi_obj = ROIOval(100, 25, 150, 50, name='oval_test')
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
        self.assertEqual(roi_obj.name, 'oval_test')

    def test_decoder_polygon(self):
        with ROIDecoder(os.path.join(directory, 'polygon.roi')) as roi:
            roi_obj = roi.get_roi()

        self.assertIsInstance(roi_obj, ROIPolygon)
        self.assertEqual(roi_obj.top, 81)
        self.assertEqual(roi_obj.left, 34)
        self.assertEqual(roi_obj.bottom, 126)
        self.assertEqual(roi_obj.right, 86)
        self.assertTrue(np.allclose([6, 0, 35, 51, 25, 14], roi_obj.x_coords))
        self.assertTrue(np.allclose([14, 44, 42, 17, 1, 0], roi_obj.y_coords))

    def test_encoder_polygon(self):
        y_coords = np.array([45, 30, 0, 12, 20])
        x_coords = np.array([0, 13, 25, 60, 5])
        left = 22
        top = 30

        right = left + np.max(x_coords) - np.min(x_coords) + 1
        bottom = top + np.max(y_coords) - np.min(y_coords) + 1

        roi_obj = ROIPolygon(top, left, bottom, right, x_coords, y_coords, name='polygon_test')
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
        self.assertEqual('polygon_test', roi_obj.name)

    def test_decoder_line(self):
        with ROIDecoder(os.path.join(directory, 'line.roi')) as roi:
            roi_obj = roi.get_roi()
        self.assertIsInstance(roi_obj, ROILine)
        self.assertEqual(roi_obj.x1, 134.75)
        self.assertEqual(roi_obj.y1, 254.0)
        self.assertEqual(roi_obj.x2, 195.75)
        self.assertEqual(roi_obj.y2, 289.625)
        self.assertEqual(roi_obj.name, 'line')

    def test_encoder_line(self):
        x1, y1, x2, y2 = 23., 256., 200, 305.
        roi_obj = ROILine(x1, y1, x2, y2, name='Line_test')
        temp_path = tempfile.mkstemp()[1]

        with ROIEncoder(temp_path, roi_obj) as roi:
            roi.write()

        with ROIDecoder(temp_path) as roi:
            roi_obj_read = roi.get_roi()

        self.assertIsInstance(roi_obj_read, ROILine)
        self.assertEqual(roi_obj_read.x1, x1)
        self.assertEqual(roi_obj_read.x2, x2)
        self.assertEqual(roi_obj_read.y1, y1)
        self.assertEqual(roi_obj_read.y2, y2)
        self.assertEqual(roi_obj_read.name, 'Line_test')
        self.assertEqual(roi_obj_read.area, 0)

    def test_decoder_polyline(self):
        with ROIDecoder(os.path.join(directory, 'polyline.roi')) as roi:
            roi_obj = roi.get_roi()
        self.assertIsInstance(roi_obj, ROIPolyline)
        self.assertEqual(len(roi_obj.x_coords), 8)
        self.assertEqual(roi_obj.name, 'polyline')

    def test_encoder_polyline(self):
        x_coords = np.array([1, 2, 3, 10, 15])
        y_coords = np.array([4, 5, 6, 8, 20])
        roi_obj = ROIPolyline(20, 40, 20 + x_coords.max(), 40 + y_coords.max(), x_coords, y_coords, name='polyline_test')
        temp_path = 'temp_file.roi'

        with ROIEncoder(temp_path, roi_obj) as roi:
            roi.write()

        with ROIDecoder(temp_path) as roi:
            roi_obj_read = roi.get_roi()

        self.assertIsInstance(roi_obj_read, ROIPolyline)
        self.assertEqual(roi_obj_read.top, 20)
        self.assertEqual(roi_obj_read.left, 40)
        self.assertTrue(np.allclose(roi_obj_read.x_coords, x_coords))
        self.assertTrue(np.allclose(roi_obj_read.y_coords, y_coords))
        self.assertEqual(roi_obj_read.name, 'polyline_test')

        os.remove(temp_path)


if __name__ == '__main__':
    unittest.main()