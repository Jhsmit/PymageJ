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

from pymagej.roi import ROIEncoder, ROIDecoder, ROIPolygon, ROIRect, ROIOval, ROILine, ROIFreeLine, ROIPolyline, \
    ROINoRoi, ROIFreehand, ROITraced, ROIAngle, ROIPoint


class MyTestCase(unittest.TestCase):
    def assertArrayEqual(self, it1, it2):
        np.testing.assert_array_equal(it1, it2)


class ROITest(MyTestCase):

    #todo top appears to be 48 in ImageJ, different coordinate system?
    #is it only top?
    def test_decoder_polygon(self):
        with ROIDecoder('polygon.roi') as roi:
            roi_obj = roi.get_roi()
        self.assertIsInstance(roi_obj, ROIPolygon)
        self.assertEqual(roi_obj.top, 49)
        self.assertEqual(roi_obj.left, 120)
        self.assertEqual(roi_obj.bottom, 137)
        self.assertEqual(roi_obj.right, 228)
        print(roi_obj.width)
        print(roi_obj.left - roi_obj.right)
        #todo figure out this difference
        self.assertEqual(len(roi_obj.x_coords), 9)
        self.assertEqual(len(roi_obj.y_coords), 9)
        self.assertArrayEqual(roi_obj.x_coords, np.array([29, 19, 55, 89, 93, 107, 108, 0, 4]))
        self.assertArrayEqual(roi_obj.y_coords, np.array([56, 88, 86, 37, 76, 70,  0, 17, 46]))

    def test_encoder_polygon(self):
        x_coords = [1, 2, 3]
        y_coords = [4, 5, 6]
        roi_obj = ROIPolygon(20, 40, x_coords, y_coords, name='polygon_test')
        temp_path = 'temp_file.roi'

        with ROIEncoder(temp_path, roi_obj) as roi:
            roi.write()

        with ROIDecoder(temp_path) as roi:
            roi_obj_read = roi.get_roi()

        self.assertIsInstance(roi_obj_read, ROIPolygon)
        self.assertEqual(roi_obj_read.top, 20)
        self.assertEqual(roi_obj_read.left, 40)
        self.assertArrayEqual(roi_obj_read.x_coords, x_coords)
        self.assertArrayEqual(roi_obj_read.y_coords, y_coords)
        self.assertEqual(roi_obj_read.name, 'polygon_test')

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

    def test_decoder_oval(self):
        with ROIDecoder('oval.roi') as roi:
            roi_obj = roi.get_roi()
        self.assertIsInstance(roi_obj, ROIOval)
        self.assertEqual(roi_obj.width, 61)
        self.assertEqual(roi_obj.height, 33)
        self.assertEqual(roi_obj.left, 143)
        self.assertEqual(roi_obj.bottom, 248)
        self.assertEqual(roi_obj.right, 204)
        self.assertEqual(roi_obj.name, 'oval')

    def test_encoder_oval(self):
        top, left, bottom, right = 230, 240, 255, 280
        roi_obj = ROIOval(top, left, bottom, right, name='Oval_test')
        temp_path = 'temp_file.roi'

        with ROIEncoder(temp_path, roi_obj) as roi:
            roi.write()

        with ROIDecoder(temp_path) as roi:
            roi_obj_read = roi.get_roi()

        self.assertIsInstance(roi_obj_read, ROIOval)
        self.assertEqual(roi_obj_read.top, top)
        self.assertEqual(roi_obj_read.left, left)
        self.assertArrayEqual(roi_obj_read.bottom, bottom)
        self.assertArrayEqual(roi_obj_read.right, right)
        self.assertEqual(roi_obj_read.name, 'Oval_test')
        self.assertEqual(roi_obj_read.area, roi_obj.area)

    def test_decoder_line(self):
        with ROIDecoder('line.roi') as roi:
            roi_obj = roi.get_roi()
        self.assertIsInstance(roi_obj, ROILine)
        self.assertEqual(roi_obj.x1, 134.75)
        self.assertEqual(roi_obj.y1, 254.0)
        self.assertEqual(roi_obj.x2, 195.75)
        self.assertEqual(roi_obj.y2, 289.625)
        self.assertEqual(roi_obj.name, 'line')

    def test_encoder_line(self):
        x1, y1, x2, y2 = 23.5, 256.8, 200, 305.756
        roi_obj = ROILine(x1, y1, x2, y2, name='Line_test')
        temp_path = 'temp_file.roi'

        with ROIEncoder(temp_path, roi_obj) as roi:
            roi.write()

        with ROIDecoder(temp_path) as roi:
            roi_obj_read = roi.get_roi()

        self.assertIsInstance(roi_obj_read, ROILine)
        self.assertEqual(roi_obj_read.x1, x1)
        self.assertEqual(roi_obj_read.x2, x2)
        self.assertAlmostEqual(roi_obj_read.y1, y1, places=1)
        self.assertAlmostEqual(roi_obj_read.y2, y2, places=1)
        #todo warn about inaccuracy?
        self.assertEqual(roi_obj_read.name, 'Line_test')
        self.assertEqual(roi_obj_read.area, 0)

    def test_decoder_freehand(self):
        with ROIDecoder('freehand.roi') as roi:
            roi_obj = roi.get_roi()
        self.assertIsInstance(roi_obj, ROIFreehand)
        self.assertEqual(len(roi_obj.x_coords), 130)
        self.assertEqual(roi_obj.name, 'freehand')

    def test_encoder_freehand(self):
        x_coords = [1, 2, 3, 10, 15]
        y_coords = [4, 5, 6, 8, 20]
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

    def test_decoder_freeline(self):
        with ROIDecoder('freehand_line.roi') as roi:
            roi_obj = roi.get_roi()
        self.assertIsInstance(roi_obj, ROIFreeLine)

    def test_encoder_freeline(self):
        x_coords = [1, 2, 3, 10, 15]
        y_coords = [4, 5, 6, 8, 20]
        roi_obj = ROIFreeLine(20, 40, x_coords, y_coords, name='freeline_test')
        temp_path = 'temp_file.roi'

        with ROIEncoder(temp_path, roi_obj) as roi:
            roi.write()

        with ROIDecoder(temp_path) as roi:
            roi_obj_read = roi.get_roi()

        self.assertIsInstance(roi_obj_read, ROIFreeLine)
        self.assertEqual(roi_obj_read.top, 20)
        self.assertEqual(roi_obj_read.left, 40)
        self.assertArrayEqual(roi_obj_read.x_coords, x_coords)
        self.assertArrayEqual(roi_obj_read.y_coords, y_coords)
        self.assertEqual(roi_obj_read.name, 'freeline_test')

        os.remove(temp_path)

    def test_decoder_polyline(self):
        with ROIDecoder('polyline.roi') as roi:
            roi_obj = roi.get_roi()
        self.assertIsInstance(roi_obj, ROIPolyline)
        self.assertEqual(len(roi_obj.x_coords), 18)
        self.assertEqual(roi_obj.name, 'polyline')

    def test_encoder_polyline(self):
        x_coords = [1, 2, 3, 10, 15]
        y_coords = [4, 5, 6, 8, 20]
        roi_obj = ROIPolyline(20, 40, x_coords, y_coords, name='polyline_test')
        temp_path = 'temp_file.roi'

        with ROIEncoder(temp_path, roi_obj) as roi:
            roi.write()

        with ROIDecoder(temp_path) as roi:
            roi_obj_read = roi.get_roi()

        self.assertIsInstance(roi_obj_read, ROIPolyline)
        self.assertEqual(roi_obj_read.top, 20)
        self.assertEqual(roi_obj_read.left, 40)
        self.assertArrayEqual(roi_obj_read.x_coords, x_coords)
        self.assertArrayEqual(roi_obj_read.y_coords, y_coords)
        self.assertEqual(roi_obj_read.name, 'polyline_test')

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

    def test_encoder_rounded_rect(self):
        pass

    def test_decoder_header(self):
        with ROIDecoder('rect_slice4.roi') as roi:
            roi_obj = roi.get_roi()
        self.assertIsInstance(roi_obj, ROIRect)
        self.assertEqual(roi_obj.top, 67)
        self.assertEqual(roi_obj.left, 124)
        self.assertEqual(roi_obj.bottom, 130)
        self.assertEqual(roi_obj.right, 187)
        self.assertEqual(roi_obj.name, 'rect_slice4')
        self.assertEqual(roi_obj.header['POSITION'] , 4)

    def test_encoder_header(self):
        roi_obj_write = ROIRect(20, 30, 40, 50, name='test_name_header')
        temp_path = 'temp_file.roi'
        roi_obj_write.header = {
            'C_POSITION': 1,
            'Z_POSITION': 2,
            'T_POSITION': 3,
            'POSITION': 4
        }

        with ROIEncoder(temp_path, roi_obj_write) as roi:
            roi.write()

        with ROIDecoder(temp_path) as roi:
            roi_obj_read = roi.get_roi()

        self.assertIsInstance(roi_obj_read, ROIRect)
        self.assertEqual(roi_obj_read.top, 20)
        self.assertEqual(roi_obj_read.left, 30)
        self.assertEqual(roi_obj_read.bottom, 40)
        self.assertEqual(roi_obj_read.right, 50)
        self.assertEqual(roi_obj_read.name, 'test_name_header')
        #todo name not properly displayed if loaded into imagej (issue)

        self.assertEqual(roi_obj_read.header['C_POSITION'], 1)
        self.assertEqual(roi_obj_read.header['Z_POSITION'], 2)
        self.assertEqual(roi_obj_read.header['T_POSITION'], 3)
        self.assertEqual(roi_obj_read.header['POSITION'], 4)

    def test_encoder_header_imagej(self):
        roi_obj_write = ROIRect(20, 30, 40, 50, name='test_name_header')
        temp_path = 'temp_zpos_imagej.roi'
        roi_obj_write.header = {
            'Z_POSITION': 2,
        }

        with ROIEncoder(temp_path, roi_obj_write) as roi:
            roi.write()

        #os.remove(temp_path)

if __name__ == '__main__':
    unittest.main()