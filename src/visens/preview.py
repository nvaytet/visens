import numpy as np
import matplotlib.pyplot as plt
from .load import load
from .image import image
from .tof import tof
from .xy_vs_tof import x_vs_tof, y_vs_tof


def preview(filename=None, data=None, save=None, **kwargs):
    """
    Make a 4-panel file preview
    """

    if data is None:
        data = load(filename, ids=True, tofs=True, convert_ids=False, **kwargs)

    fig, ax = plt.subplots(2, 2, figsize=(12, 9))
    fig.suptitle(filename.split("/")[-1])

    tof(data=data, ax=ax[0][0], **kwargs)
    x_vs_tof(data=data, ax=ax[0][1], log=True, **kwargs)
    image(data=data, ax=ax[1][0], side_panels=False, log=True, **kwargs)
    y_vs_tof(data=data, ax=ax[1][1], log=True, **kwargs)

    if save is not None:
        fig.savefig(save, bbox_inches="tight")
    else:
        plt.show()
