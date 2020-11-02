[![Build Status](https://travis-ci.com/Jhsmit/PymageJ.svg?branch=master)](https://travis-ci.com/Jhsmit/PymageJ)

# PymageJ
Python tools for ImageJ. 
Features: read/write ImageJ ROIs.

## How to use

**Reading ROI files:**

```python

from pymagej.roi import ROIDecoder

with ROIDecoder('roi_filepath.roi') as roi:
    roi_obj = roi.get_roi()
  
```

The returned ```roi_obj``` is an ROIObject depending on the type of ROI. Currently only reading rectangle and freehand are supported.

**Writing ROI files:**

```python

from pymagej.roi import ROIEncoder, ROIRect

roi_obj = ROIRect(20, 30, 40, 50) # Make ROIRect object specifing top, left, bottom, right
with ROIEncoder('roi_filepath.roi', roi_obj) as roi:
    roi.write()
  
```

Read/write is supported for the following ROI types:

- Polygon
- Rectangle
- Oval
- Line
- Freeline
- Polyline
- Freehand



Please make issues for feature requests/bug reports!
