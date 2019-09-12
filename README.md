<table>
<tr>
<td>
<h1>VISENS</h1>
<b>VIS</b>ualization for <b>E</b>SS <b>N</b>eutron <b>S</b>cience
</td>
<td><img src="https://raw.githubusercontent.com/nvaytet/visens/master/docs/images/visens_logo.png" width="200" /></td>
</tr>
</table>

### Installation:

```
pip install visens
```

### Usage:

```Python
import visens as vs

# Diffraction experiment
file1 = "V20_ESSIntegration_2018-12-13_0942_stripped.nxs"
# Reflectometry experiment
file2 = "nicos_00000447_agg_with_monitor.nxs"
```

```Python
# Plot a 2D image of the integrated detector counts
vs.image(file2)
```
![image.png](https://github.com/nvaytet/v20dataviz/raw/master/docs/images/image.png)
```Python
# Plot a x versus time-of-flight diagram
vs.x_vs_tof(file1)
```
![x_vs_tof.png](https://github.com/nvaytet/v20dataviz/raw/master/docs/images/x_vs_tof.png)
```Python
# Open a slicer plot that allows to navigate the tof dimension with mouse wheel
vs.slicer(file2)
```
![slicer.png](https://github.com/nvaytet/v20dataviz/raw/master/docs/images/slicer.png)
```Python
# 3D volume rendering (x, y, tof)
# (only available in jupyter notebook, requires ipyvolume)
vs.volume(file1)
```
![volume.png](https://github.com/nvaytet/v20dataviz/raw/master/docs/images/volume.png)
