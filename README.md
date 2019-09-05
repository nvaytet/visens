# v20dataviz

Data visualization scripts for v20

### Setup:

```
export PYTHONPATH=/path/to/v20dataviz/src:$PYTHONPATH
```

### Usage:

```Python
import v20dataviz as dv

# Diffraction experiment
file1 = "V20_ESSIntegration_2018-12-13_0942_stripped.nxs"
# Reflectometry experiment
file2 = "nicos_00000447_agg_with_monitor.nxs"
```

```Python
# Plot a 2D image of the integrated detector counts
dv.image(file2)
```
![image.png](https://github.com/nvaytet/v20dataviz/raw/master/docs/images/image.png)
```Python
# Plot a x versus time-of-flight diagram
dv.x_vs_tof(file1)
```
![x_vs_tof.png](https://github.com/nvaytet/v20dataviz/raw/master/docs/images/x_vs_tof.png)
```Python
# Open a slicer plot that allows to navigate the tof dimension with mouse wheel
dv.slicer(file2)
```
![slicer.png](https://github.com/nvaytet/v20dataviz/raw/master/docs/images/slicer.png)
```Python
# Specify the paths in nexus/hdf file
dv.slicer(file2, vmax=5,
    id_path="/entry/instrument/detector_1/raw_event_data/event_id",
    tof_path="/entry/instrument/detector_1/raw_event_data/event_time_offset")
```

```Python
# 3D volume rendering (x, y, tof)
# (only available in jupyter notebook, requires ipyvolume)
dv.volume(file1)
```
![volume.png](https://github.com/nvaytet/v20dataviz/raw/master/docs/images/volume.png)
