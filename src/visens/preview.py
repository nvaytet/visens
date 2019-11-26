import numpy as np
import matplotlib.pyplot as plt
from .load import load
from .image import image
from .tof import tof
from .xy_vs_tof import x_vs_tof, y_vs_tof


def preview(filename=None, data=None, save=None, log=False):
    """
    Make a 4-panel file preview
    """

    if data is None:
        data = load(filename, ids=True, tofs=True, convert_ids=False)

    fig, ax = plt.subplots(2, 2, figsize=(12, 9))
    fig.suptitle(filename.split("/")[-1])

    tof(data=data, ax=ax[0][0])
    x_vs_tof(data=data, ax=ax[0][1], log=log)
    image(data=data, ax=ax[1][0], side_panels=False, log=log)
    y_vs_tof(data=data, ax=ax[1][1], log=log)

    if save is not None:
        fig.savefig(save, bbox_inches="tight")
    else:
        plt.show()
