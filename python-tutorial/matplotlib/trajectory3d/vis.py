#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

def update_lines(num,data,lines):
    """ for frame number 'num', update a list of matplotlib line objects 'lines'
     with data for the given frame 'data[num]' """
    conf = data[num,:,:] # current particle configuration
    # loop through each one of the 16 dots and the 16 particles together
    for line,pos in zip(lines,conf):
        x,y,z = pos
        line.set_data(x,y)
        line.set_3d_properties(z)
    # end for
# end def update_lines

if __name__ == '__main__':

    ndim = 3

    # local particle positions, must have shape (nframe,natom*ndim)
    data = np.loadtxt('nxyz.dat')
    nframe,nad = data.shape
    natom = nad/ndim
    data = data.reshape(nframe,natom,ndim)

    # Attach 3D axis to the figure
    fig = plt.figure()
    ax = p3.Axes3D(fig)

    # make first frame: 16 dots, one for each particle
    lines = [ax.plot( data[0,:,0], data[0,:,1], data[0,:,2], 'o' )[0] for dat in data[0]]
    #plt.show()

    # Creating the Animation object
    ani = animation.FuncAnimation(fig, update_lines, nframe, fargs=(data, lines),
                                  interval=50, blit=False)
    plt.show()
# end __main__
