#!/usr/bin/env python
from plotly.offline import plot
import plotly.graph_objs as go

import numpy as np


def gauss3d(x, y, z, sig=1.0):
    return np.exp(-(x**2+y**2+z**2)/(2*sig**2))


def get_data(nx, ny, nz):
    # define 3D grid
    x = np.linspace(-1, 1, nx)
    y = np.linspace(-1, 1, ny)
    z = np.linspace(-1, 1, nz)

    # grid basis
    dx = x[1]-x[0]
    dy = y[1]-y[0]
    dz = z[1]-z[0]
    axes = np.diag([dx, dy, dz])

    # evaluate Gaussian on grid
    from itertools import product
    xyz = np.array(list(product(x, y, z)))
    vals = np.array([
        gauss3d(myx, myy, myz) for (myx, myy, myz) in product(x, y, z)
    ])
    return axes, xyz, vals


def get_regular_grid_dimensions(gvecs):
    gmin = gvecs.min(axis=0)
    gmax = gvecs.max(axis=0)
    ng = np.around(gmax-gmin+1).astype(int)
    return gmin, gmax, ng


def get_zslice(xyz, vals, zval):
    # need grid to be defined:
    #  nx, ny, z

    # select slices
    sel = np.abs(xyz[:, 2]-zval)<dz/2.
    myxyz = xyz[sel]
    myvals = vals[sel]

    # put slice on 2D regular grid
    xx = myxyz[:, 0].reshape(nx, ny)
    yy = myxyz[:, 1].reshape(nx, ny)
    zz = myxyz[:, 2].reshape(nx, ny)

    zslice = go.Surface(
      x=xx, y=yy, z=zz, surfacecolor=myvals.reshape(nx, ny),
      colorscale='Viridis', showscale=True
    )
    zslice.update(cmin=vals.min(), cmax=vals.max())
    return zslice

if __name__ == '__main__':
    nx = 12
    ny = 8
    nz = 16

    # data must be given on a regular grid
    axes, xyz, vals = get_data(nx, ny, nz)

    # recover grid labels
    dx, dy, dz = np.diag(axes)
    upos = np.dot(xyz, np.linalg.inv(axes))
    umin, umax, un = get_regular_grid_dimensions(upos)
    x = np.linspace(umin[0], umax[0], un[0])*dx
    y = np.linspace(umin[1], umax[1], un[1])*dy
    z = np.linspace(umin[2], umax[2], un[2])*dz

    ## plot one slice
    #zval = z[5]
    #zslice = get_zslice(zval)
    #plot([zslice])

    # plot all slices
    frames = [{'data': [get_zslice(xyz, vals, zval)]} for zval in z]
    layout = {
      'scene': {
        'zaxis': go.layout.scene.ZAxis(range=[-1, 1])
      }
    }
    fig = {
      'data': frames[0]['data'],
      'frames': frames[1:],
      'layout': layout
    }
    plot(fig)

# end __main__
