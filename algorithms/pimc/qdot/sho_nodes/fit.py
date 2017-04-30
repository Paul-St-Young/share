#!/usr/bin/env python
import numpy as np
def exp(x,A,alpha):
    return A*np.exp(alpha*x*x)
def quadratic(x,a,b,c):
    return a*x*x+b*x+c
def quartic(x,a,b):
    return a*x**4.+b*x

if __name__ == '__main__':

    myx,myy = np.loadtxt('relation.dat').T

    model = quartic
    import scipy.optimize as op
    popt,pcov = op.curve_fit(quartic,myx,myy)
    fit = np.polyfit(myx,myy,deg=4)
    print np.poly1d(fit)

    import matplotlib.pyplot as plt
    fig,ax = plt.subplots(1,1)
    ax.plot(myx,myy,'o')
    ax.plot(myx,model(myx,*popt))
    #ax.plot(myx,np.poly1d(fit)(myx))
    plt.show()
