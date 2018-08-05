#!/usr/bin/env python
from plotly.offline import plot
import plotly.graph_objs as go

import numpy as np

def gauss3d(x, y, z, sig=1.0):
    return np.exp(-(x**2+y**2+z**2)/(2*sig**2))

def get_zslice(zval):
    xx, yy = np.meshgrid(x, y)
    zz = np.zeros(xx.shape)
    zz[:, :] = zval
    vals = gauss3d(xx, yy, zz)

    zslice = go.Surface(
      x=xx, y=yy, z=zz, surfacecolor=vals,
      colorscale='Viridis', showscale=True)
    zslice.update(cmin=0, cmax=1)
    return zslice

if __name__ == '__main__':
    nx = 16
    x = np.linspace(-1, 1, nx)
    y = np.linspace(-1, 1, nx)

    nz = 16
    z = np.linspace(-1, 1, nz)

    frames = [
      {'data': [get_zslice(zval)]}
      for zval in z]

    layout = dict(
      scene = dict(
        zaxis=go.layout.scene.ZAxis(range=[-1, 1])
      )
    )

    fig = dict(
      data=frames[0]['data'],
      layout=layout,
      frames=frames
    )

    plot(fig)
# end __main__
