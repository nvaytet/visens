# v20dataviz

Data visualization scripts for v20

### Setup:

```
export PYTHONPATH=/path/to/v20dataviz/src:$PYTHONPATH
```

### Usage:

```Python
import v20dataviz as dv

filename = 'V20_ESSIntegration_2018-12-13_0942_stripped.nxs'

# Plot a 2D image of the integrated detector counts
dv.image(filename)

# Plot a x versus time-of-flight diagram
dv.x_vs_tof(filename)

# Open a slicer plot that allows to navigate the tof dimension with mouse wheel
dv.slicer(filename)

# Specify the paths in nexus/hdf file
dv.slicer(fname, vmax=5,
    id_path="/entry/instrument/detector_1/raw_event_data/event_id",
    tof_path="/entry/instrument/detector_1/raw_event_data/event_time_offset")

# 3D volume rendering (x, y, tof)
# (only available in jupyter notebook, requires ipyvolume)
dv.volume(fname)
```
