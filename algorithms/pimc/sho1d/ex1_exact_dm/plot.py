#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

def analytic_x2(omega,beta):
    """ mean square deviation of 1D SHO with unit mass """
    return 1./(2*omega)*1./np.tanh(beta*omega/2.)

if __name__ == '__main__':

    data = np.loadtxt('x2_omega.dat')
    myx  = data[:,0] # omega
    myy  = data[:,5] # mean of  <x^2>
    myye = data[:,6] # error of <x^2>
    
    finex = np.linspace(myx[0],myx[-1],100)

    fig,ax = plt.subplots(1,1)
    ax.set_xlabel('omega')
    ax.set_ylabel('x2')
    ax.errorbar(myx,myy,yerr=myye,fmt='x',label='sampled')
    ax.plot(finex,analytic_x2(finex,1.0),c='k',label='exact')
    ax.legend()
    ax.set_xlim(myx[0]-1,myx[-1]+1)
    plt.show()
