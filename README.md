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

Currently only writing of rectangle type ROI is supported.

Please make issues for feature requests/bug reports!
