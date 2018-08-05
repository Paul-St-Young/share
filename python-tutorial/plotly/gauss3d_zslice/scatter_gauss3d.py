#!/usr/bin/env python
from plotly.offline import plot
import plotly.graph_objs as go

import numpy as np


def gauss3d(x, y, z, sig=1.0):
    return np.exp(-(x**2+y**2+z**2)/(2*sig**2))


def color_scatter(xyz, vals):
    marker = dict(
      color=vals,
      colorscale='Viridis',
      opacity=0.8,
      size=2,
    )
    x, y, z = xyz.T
    scatter = go.Scatter3d(
      mode='markers',
      x=x, y=y, z=z, marker=marker)
    return scatter


if __name__ == '__main__':
    # define 3D grid
    nx = 16
    x = np.linspace(-1, 1, nx)
    y = np.linspace(-1, 1, nx)
    z = np.linspace(-1, 1, nx)

    # evaluate Gaussian on grid
    from itertools import product
    xyz = np.array(list(product(x, y, z)))
    vals = np.array([
        gauss3d(myx, myy, myz) for (myx, myy, myz) in product(x, y, z)
    ])

    # plot Gaussian
    sel = (vals > 0.5)
    scatter = color_scatter(xyz[sel], vals[sel])
    plot([scatter])
# end __main__
