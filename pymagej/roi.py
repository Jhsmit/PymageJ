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
import struct
import re
from collections import namedtuple
import os


# http://rsb.info.nih.gov/ij/developer/source/ij/io/RoiDecoder.java.html
# http://rsb.info.nih.gov/ij/developer/source/ij/io/RoiEncoder.java.html


#  Base class for all ROI classes
class ROIObject(object):

    def __init__(self, name=None):
        self.name = name

    def area(self):
        raise NotImplementedError('Area not implemented')


class ROIPolygon(ROIObject):
    type = 'polygon'

    def __init__(self, top, left, bottom, right, x_coords, y_coords, *args, **kwargs):
        super(ROIPolygon, self).__init__(*args, **kwargs)
        self.top = top
        self.left = left
        self.bottom = bottom
        self.right = right
        self.x_coords = x_coords
        self.y_coords = y_coords

    @property
    def width(self):
        return self.x_coords.max() - self.x_coords.min() + 1

    @property
    def height(self):
        return self.y_coords.max() - self.y_coords.min() + 1

    def __len__(self):
        return len(self.x_coords)


class ROIRect(ROIObject):
    type = 'rect'

    def __init__(self, top, left, bottom, right, arc=0, *args, **kwargs):
        super(ROIRect, self).__init__(*args, **kwargs)
        self.top = top
        self.left = left
        self.bottom = bottom
        self.right = right
        self.arc = arc

    @property
    def width(self):
        return self.right - self.left

    @property
    def height(self):
        return self.bottom - self.top

    @property
    def area(self):
        if self.arc == 0:
            return self.width * self.height
        else:
            return self.width * self.height - ((4 - np.pi)*(self.arc/2.)**2)


class ROIOval(ROIObject):
    type = 'oval'

    def __init__(self, top, left, bottom, right, *args, **kwargs):
        super(ROIOval, self).__init__(*args, **kwargs)
        self.top = top
        self.left = left
        self.bottom = bottom
        self.right = right

    @property
    def width(self):
        return self.right - self.left

    @property
    def height(self):
        return self.bottom - self.top

    @property
    def area(self):
        return self.width * self.height * np.pi / 4


class ROILine(ROIObject):
    type = 'line'

    def __init__(self, x1, y1, x2, y2, *args, **kwargs):
        super(ROILine, self).__init__(*args, **kwargs)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    @property
    def area(self):
        return 0


class ROIFreeLine(ROIObject):
    type = 'freeline'

    def __init__(self, top, left, bottom, right, x_coords, y_coords, *args, **kwargs):
        super(ROIFreeLine, self).__init__(*args, **kwargs)
        assert (len(x_coords) == len(y_coords)), 'Unequal length of x and y coords'
        self.top = top
        self.left = left
        self.bottom = bottom
        self.right = right
        self.x_coords = np.array(x_coords)
        self.y_coords = np.array(y_coords)

    @property
    def width(self):
        return self.x_coords.max() - self.x_coords.min() + 1

    @property
    def height(self):
        return self.y_coords.max() - self.y_coords.min() + 1

    @property
    def area(self):
        raise NotImplementedError("Freeline area not implemented")

    def __len__(self):
        return len(self.x_coords)


class ROIPolyline(ROIObject):
    type = 'polyline'

    def __init__(self, top, left, bottom, right, x_coords, y_coords, *args, **kwargs):
        super(ROIPolyline, self).__init__(*args, **kwargs)
        assert(len(x_coords) == len(y_coords))
        self.top = top
        self.left = left
        self.bottom = bottom
        self.right = right
        self.x_coords = np.array(x_coords)
        self.y_coords = np.array(y_coords)

    @property
    def width(self):
        return self.x_coords.max() - self.x_coords.min() + 1

    @property
    def height(self):
        return self.y_coords.max() - self.y_coords.min() + 1

    @property
    def area(self):
        raise NotImplementedError("Freeline area not implemented")

    def __len__(self):
        return len(self.x_coords)


class ROINoRoi(ROIObject):
    type = 'no_roi'

    @property
    def area(self):
        return 0


class ROIFreehand(ROIObject):
    type = 'freehand'

    def __init__(self, top, left, bottom, right, x_coords, y_coords, *args, **kwargs):
        super(ROIFreehand, self).__init__(*args, **kwargs)
        self.top = top
        self.left = left
        self.bottom = bottom
        self.right = right
        self.x_coords = x_coords
        self.y_coords = y_coords

    def __len__(self):
        return len(self.x_coords)

    @property
    def width(self):
        return self.x_coords.max() - self.x_coords.min() + 1

    @property
    def height(self):
        return self.y_coords.max() - self.y_coords.min() + 1

    @property
    def area(self):
        raise NotImplementedError('Area of freehand ROI is not implemented')


class ROITraced(ROIObject):
    type = 'traced'

    def __init__(self, top, left, bottom, right, x_coords, y_coords, *args, **kwargs):
        super(ROITraced, self).__init__(*args, **kwargs)
        self.top = top
        self.left = left
        self.bottom = bottom
        self.right = right
        self.x_coords = x_coords
        self.y_coords = y_coords

    @property
    def width(self):
        return self.x_coords.max() - self.x_coords.min() + 1

    @property
    def height(self):
        return self.y_coords.max() - self.y_coords.min() + 1

    @property
    def area(self):
        raise NotImplementedError('Area of traced ROI is not implemented')


class ROIAngle(ROIObject):
    @property
    def area(self):
        return 0


class ROIPoint(ROIObject):
    @property
    def area(self):
        return 0


HeaderTuple = namedtuple('Header_variables', 'type size offset')


class ROIFileObject(object):
    header1_fields = [
        # 'VAR_NAME', 'type', offset'
        ['MAGIC', '4s', 0],
        ['VERSION_OFFSET', 'h', 4],
        ['TYPE', 'b', 6],
        ['TOP', 'h', 8],
        ['LEFT', 'h', 10],
        ['BOTTOM', 'h', 12],
        ['RIGHT', 'h', 14],
        ['N_COORDINATES', 'h', 16],
        ['X1', 'f', 18],
        ['Y1', 'f', 22],
        ['X2', 'f', 26],
        ['Y2', 'f', 30],
        ['XD', 'f', 18],  # D vars for sub pixel resolution ROIs
        ['YD', 'f', 22],
        ['WIDTH', 'f', 26],
        ['HEIGHT', 'f', 30],
        ['STROKE_WIDTH', 'h', 34],
        ['SHAPE_ROI_SIZE', 'i', 36],
        ['STROKE_COLOR', 'i', 40],
        ['FILL_COLOR', 'i', 44],
        ['SUBTYPE', 'h', 48],
        ['OPTIONS', 'h', 50],
        ['ARROW_STYLE', 'b', 52],
        ['ELLIPSE_ASPECT_RATIO', 'b', 52],
        ['POINT_TYPE', 'b', 52],
        ['ARROW_HEAD_SIZE', 'b', 53],
        ['ROUNDED_RECT_ARC_SIZE', 'h', 54],
        ['POSITION', 'i', 56],
        ['HEADER2_OFFSET', 'i', 60]
        #['COORDINATES', 'i', 64]
    ]

    header2_fields = [
        ['C_POSITION', 'i', 4],
        ['Z_POSITION', 'i', 8],
        ['T_POSITION', 'i', 12],
        ['NAME_OFFSET', 'i', 16],
        ['NAME_LENGTH', 'i', 20],
        ['OVERLAY_LABEL_COLOR', 'i', 24],
        ['OVERLAY_FONT_SIZE', 'h', 28],
        ['AVAILABLE_BYTE1', 'b', 30],
        ['IMAGE_OPACITY', 'b', 31],
        ['IMAGE_SIZE', 'i', 32],
        ['FLOAT_STROKE_WIDTH', 'f', 36],
        ['ROI_PROPS_OFFSET', 'i', 40],
        ['ROI_PROPS_LENGTH', 'i', 44]
    ]

    roi_types_rev = {'polygon': 0, 'rect': 1, 'oval': 2, 'line': 3, 'freeline': 4, 'polyline': 5, 'no_roi': 6,
                     'freehand': 7, 'traced': 8, 'angle': 9, 'point': 10}

    roi_types = {0: 'polygon', 1: 'rect', 2: 'oval', 3: 'line', 4: 'freeline', 5: 'polyline', 6: 'no_roi',
                 7: 'freehand', 8: 'traces', 9: 'angle', 10: 'point'}

    @staticmethod
    def _type_size(_type):
        sizes = {'h': 2, 'f': 4, 'i': 4, 's': 1, 'b': 1}
        char = re.findall('\\D', _type)[0]
        size = sizes[char]
        number = re.findall('\\d', _type)

        if number:
            size *= int(number[0])
        return size


class ROIEncoder(ROIFileObject):

    def __init__(self, path, roi_obj):
        self.path = path
        self.roi_obj = roi_obj

        self._header1_dict = {e[0]: HeaderTuple(e[1], self._type_size(e[1]), e[2]) for e in self.header1_fields}
        self._header2_dict = {e[0]: HeaderTuple(e[1], self._type_size(e[1]), e[2]) for e in self.header2_fields}

    def write(self):

        self._write_var('MAGIC', b'Iout')
        self._write_var('VERSION_OFFSET', 225)  # todo or 226??

        roi_writer = getattr(self, '_write_roi_' + self.roi_obj.type)
        roi_writer()

    def __enter__(self):
        self.f_obj = open(self.path, 'wb')
        pad = struct.pack('128b', *np.zeros(128, dtype=int))
        self.f_obj.write(pad)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.f_obj.close()
        return False

    def _write_roi_polygon(self):
        self._write_var('TYPE', self.roi_types_rev[self.roi_obj.type])
        self._write_var('TOP', self.roi_obj.top)
        self._write_var('LEFT', self.roi_obj.left)
        self._write_var('BOTTOM', self.roi_obj.bottom)
        self._write_var('RIGHT', self.roi_obj.right)
        self._write_var('HEADER2_OFFSET', self.header2_offset)
        self._write_var('NAME_OFFSET', self.name_offset)

        self._write_coords(np.concatenate((self.roi_obj.x_coords, self.roi_obj.y_coords)))
        self._write_name()

    def _write_roi_rect(self):
        self._write_var('TYPE', self.roi_types_rev[self.roi_obj.type])
        self._write_var('TOP', self.roi_obj.top)
        self._write_var('LEFT', self.roi_obj.left)
        self._write_var('BOTTOM', self.roi_obj.bottom)
        self._write_var('RIGHT', self.roi_obj.right)
        self._write_var('HEADER2_OFFSET', self.header2_offset)
        self._write_var('NAME_OFFSET', self.name_offset)
        self._write_name()

    def _write_roi_oval(self):
        #todo call write rect-like function
        self._write_var('TYPE', self.roi_types_rev[self.roi_obj.type])
        self._write_var('TOP', self.roi_obj.top)
        self._write_var('LEFT', self.roi_obj.left)
        self._write_var('BOTTOM', self.roi_obj.bottom)
        self._write_var('RIGHT', self.roi_obj.right)
        self._write_var('HEADER2_OFFSET', self.header2_offset)
        self._write_var('NAME_OFFSET', self.name_offset)
        self._write_name()

    def _write_roi_line(self):
        self._write_var('TYPE', self.roi_types_rev[self.roi_obj.type])

        for var_name, attr_name in zip(['X1', 'Y1', 'X2', 'Y2'], ['x1', 'y1', 'x2', 'y2']):
            self._write_var(var_name, getattr(self.roi_obj, attr_name))

        self._write_var('HEADER2_OFFSET', self.header2_offset)
        self._write_var('NAME_OFFSET', self.name_offset)
        self._write_name()

    def _write_roi_freeline(self):
        self._write_var('TYPE', self.roi_types_rev[self.roi_obj.type])
        self._write_var('TOP', self.roi_obj.top)
        self._write_var('LEFT', self.roi_obj.left)
        self._write_var('BOTTOM', self.roi_obj.bottom)
        self._write_var('RIGHT', self.roi_obj.right)
        self._write_var('N_COORDINATES', len(self.roi_obj))
        self._write_var('HEADER2_OFFSET', self.header2_offset)
        self._write_var('NAME_OFFSET', self.name_offset)

        self._write_coords(np.concatenate((self.roi_obj.x_coords, self.roi_obj.y_coords)))
        self._write_name()

    def _write_roi_polyline(self):
        self._write_var('TYPE', self.roi_types_rev[self.roi_obj.type])
        self._write_var('TOP', self.roi_obj.top)
        self._write_var('LEFT', self.roi_obj.left)
        self._write_var('BOTTOM', self.roi_obj.bottom)
        self._write_var('RIGHT', self.roi_obj.right)
        self._write_var('N_COORDINATES', len(self.roi_obj))
        self._write_var('HEADER2_OFFSET', self.header2_offset)
        self._write_var('NAME_OFFSET', self.name_offset)

        self._write_coords(np.concatenate((self.roi_obj.x_coords, self.roi_obj.y_coords)))
        self._write_name()

    def _write_roi_no_roi(self):
        raise NotImplementedError('Writing roi type no roi is not implemented')

    def _write_roi_freehand(self):
        self._write_var('TYPE', self.roi_types_rev[self.roi_obj.type])
        self._write_var('TOP', self.roi_obj.top)
        self._write_var('LEFT', self.roi_obj.left)
        self._write_var('BOTTOM', self.roi_obj.bottom)
        self._write_var('RIGHT', self.roi_obj.right)
        self._write_var('N_COORDINATES', len(self.roi_obj))
        self._write_var('HEADER2_OFFSET', self.header2_offset)
        self._write_var('NAME_OFFSET', self.name_offset)

        self._write_coords(np.concatenate((self.roi_obj.x_coords, self.roi_obj.y_coords)))
        self._write_name()

    def _write_roi_traced(self):
        raise NotImplementedError('Writing roi type traced is not implemented')

    def _write_roi_angle(self):
        raise NotImplementedError('Writing roi type angle is not implemented')

    def _write_roi_point(self):
        raise NotImplementedError('Writing roi type point is not implemented')

    def _write_var(self, var_name, value):
        if var_name in self._header1_dict:
            var = self._header1_dict[var_name]
            offset = var.offset
        elif var_name in self._header2_dict:
            var = self._header2_dict[var_name]
            offset = var.offset + self.header2_offset
        else:
            raise Exception('Header variable %s not found' % var_name)

        self.f_obj.seek(offset)
        binary = struct.pack('>' + var.type, value)
        self.f_obj.write(binary)

    def _write_name(self):
        if self.roi_obj.name:
            name = self.roi_obj.name
        else:
            name = os.path.basename(
                os.path.splitext(self.path)[0]
            )

        self._write_var('NAME_LENGTH', len(name))
        name = ''.join(i for j in zip(len(name)*' ', name) for i in j)  # interleave with with spaces

        self.f_obj.seek(self.name_offset)
        self.f_obj.write(name.encode())

    def _write_coords(self, coords):
        n_coords = int(len(coords) / 2)
        self._write_var('N_COORDINATES', n_coords)
        self.f_obj.seek(64)
        binary = struct.pack('>' + str(len(coords)) + 'h', *coords)
        self.f_obj.write(binary)

    @property
    def header2_offset(self):
        if hasattr(self.roi_obj, 'x_coords'):
            return 64 + len(self.roi_obj)*2*2  # Header1 size + 2 bytes per pair of coords
        else:
            return 64

    @property
    def name_offset(self):
        return self.header2_offset + 64  # Name is after header2 which as size 6


class ROIDecoder(ROIFileObject):
    def __init__(self, roi_path):
        self.roi_path = roi_path
        self.header = {}  # Output header dict
        self._header1_dict = {e[0]: HeaderTuple(e[1], self._type_size(e[1]), e[2]) for e in self.header1_fields}
        self._header2_dict = {e[0]: HeaderTuple(e[1], self._type_size(e[1]), e[2]) for e in self.header2_fields}

    def __enter__(self):
        self.f_obj = open(self.roi_path, 'rb')
        return self

    def __exit__(self, type, value, traceback):
        self.f_obj.close()
        return False

    def read_header_all(self):
        to_read_h1 = [e[0] for e in self.header1_fields]  # Read everything in header1
        to_read_h2 = [e[0] for e in self.header2_fields]  # Read everything in header2

        for h in to_read_h1 + to_read_h2:
            self._set_header(h)

    def read_header(self):
        if self._get_var('MAGIC') != b'Iout':
            raise IOError('Invalid ROI file, magic number mismatch')

        # to_read_h1 = ['VERSION_OFFSET', 'TYPE', 'SUBTYPE', 'TOP', 'LEFT', 'BOTTOM', 'RIGHT', 'N_COORDINATES',
        #               'STROKE_WIDTH', 'SHAPE_ROI_SIZE', 'STROKE_COLOR', 'FILL_COLOR', 'SUBTYPE', 'OPTIONS', 'POSITION',
        #               'HEADER2_OFFSET']

        to_read_h1 = [e[0] for e in self.header1_fields]  # Read everything in header1
        to_read_h2 = [e[0] for e in self.header2_fields]  # Read everything in header2

        set_zero = ['OVERLAY_LABEL_COLOR', 'OVERLAY_FONT_SIZE', 'IMAGE_OPACITY']

        for h in to_read_h1 + to_read_h2:
            self._set_header(h)

        for h in set_zero:
            self.header[h] = 0

    def get_roi(self):
        if not self.header:
            self.read_header()

        try:
            roi_reader = getattr(self, '_get_roi_' + self.roi_types[self.header['TYPE']])
        except AttributeError:
            raise NotImplementedError('Reading roi type %s not implemented' % self.roi_types[self.header['TYPE']])

        roi_obj = roi_reader()
        roi_obj.name = self._get_name()
        roi_obj.header = self.header

        return roi_obj

    def _get_roi_polygon(self):
        params = ['TOP', 'LEFT', 'BOTTOM', 'RIGHT']
        for p in params:
            self._set_header(p)

        top, left, bottom, right = [self.header[p] for p in params]

        n_coords = self.header['N_COORDINATES']
        self.f_obj.seek(64)
        binary = self.f_obj.read(2 * n_coords * 2)
        coords = np.array(struct.unpack('>' + str(2 * n_coords) + 'h', binary))
        x_coords = np.array(coords[:n_coords])
        y_coords = np.array(coords[n_coords:])

        return ROIPolygon(top, left, bottom, right, x_coords, y_coords)

    def _get_roi_rect(self):
        self._set_header('ROUNDED_RECT_ARC_SIZE')
        arc = self.header['ROUNDED_RECT_ARC_SIZE']

        params = ['TOP', 'LEFT', 'BOTTOM', 'RIGHT']
        for p in params:
            self._set_header(p)

        top, left, bottom, right = [self.header[p] for p in params]

        return ROIRect(top, left, bottom, right, arc=arc)

    def _get_roi_oval(self):
        params = ['TOP', 'LEFT', 'BOTTOM', 'RIGHT']
        for p in params:
            self._set_header(p)

        top, left, bottom, right = [self.header[p] for p in params]

        return ROIOval(top, left, bottom, right)

    def _get_roi_line(self):
        params = ['X1', 'Y1', 'X2', 'Y2']
        for p in params:
            self._set_header(p)

        x1, y1, x2, y2 = [self.header[p] for p in params]

        return ROILine(x1, y1, x2, y2)

    def _get_roi_freeline(self):
        params = ['TOP', 'LEFT', 'BOTTOM', 'RIGHT']
        for p in params:
            self._set_header(p)

        top, left, bottom, right = [self.header[p] for p in params]
        coords = self._get_coords()
        x_coords, y_coords = coords.reshape(2, -1)

        return ROIFreeLine(top, left, bottom, right, x_coords, y_coords)

    def _get_roi_polyline(self):
        params = ['TOP', 'LEFT', 'BOTTOM', 'RIGHT']
        for p in params:
            self._set_header(p)

        top, left, bottom, right = [self.header[p] for p in params]
        coords = self._get_coords()
        x_coords, y_coords = coords.reshape(2, -1)

        return ROIPolyline(top, left, bottom, right, x_coords, y_coords)

    def _get_roi_no_roi(self):
        raise NotImplementedError('Reading roi type no roi is not implemented')

    def _get_roi_freehand(self):
        params = ['TOP', 'LEFT', 'BOTTOM', 'RIGHT']
        for p in params:
            self._set_header(p)

        top, left, bottom, right = [self.header[p] for p in params]
        coords = self._get_coords()
        x_coords, y_coords = coords.reshape(2, -1)

        return ROIFreehand(top, left, bottom, right, x_coords, y_coords)

    def _get_roi_traced(self):
        params = ['TOP', 'LEFT', 'BOTTOM', 'RIGHT']
        for p in params:
            self._set_header(p)

        top, left, bottom, right = [self.header[p] for p in params]
        coords = self._get_coords()
        x_coords, y_coords = coords.reshape(2, -1)

        return ROITraced(top, left, bottom, right, x_coords, y_coords)

    def _get_roi_angle(self):
        raise NotImplementedError('Reading roi type angle is not implemented')

    def _get_roi_point(self):
        raise NotImplementedError('Reading roi type point is not implemented')

    def _get_var(self, var_name):
        if var_name in self._header1_dict:
            var = self._header1_dict[var_name]
            offset = var.offset
        elif var_name in self._header2_dict:
            var = self._header2_dict[var_name]
            offset = var.offset + self._get_var('HEADER2_OFFSET')
        else:
            raise Exception('Header variable %s not found' % var_name)

        self.f_obj.seek(offset)
        binary = self.f_obj.read(var.size)
        return struct.unpack('>' + var.type, binary)[0]  # read header variable, big endian

    def _get_coords(self):
        n_coords = self.header['N_COORDINATES']
        self.f_obj.seek(64)
        binary = self.f_obj.read(2*2*n_coords)  # Two bytes per pair of coords
        coords = np.array(struct.unpack('>' + str(2*n_coords) + 'h', binary))

        return coords

    def _get_name(self):
        name_length = self._get_var('NAME_LENGTH')
        name_offset = self._get_var('NAME_OFFSET')
        self.f_obj.seek(name_offset)
        binary = self.f_obj.read(2*name_length)
        return binary.decode()[1::2]

    def _set_header(self, var_name):
        self.header[var_name] = self._get_var(var_name)
