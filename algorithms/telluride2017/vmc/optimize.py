#!/usr/bin/env python
import os
import numpy as np
from reference import metropolis_sample, Hamiltonian, test_hellium
from wavefunction import ExponentSlaterWF

def brute_slater_hellium():
    ham = Hamiltonian(Z=2)
    params = [0.5,1.0,1.5,2.0,2.5,3.0]
    taus   = [1.0,0.5,0.3,0.1,0.1,0.1]

    data = np.zeros([len(params),3]) # 3 columns for param,val,err
    for iexp in range(len(params)):
        exp = params[iexp]
        tau = taus[iexp]
        wf = ExponentSlaterWF(alpha=exp)
        val,err = test_hellium(use_drift=True,wf=wf,tau=tau)
        data[iexp,0] = exp
        data[iexp,1] = val
        data[iexp,2] = err
    
    np.savetxt('slater.dat',data)

def plot_slater_hellium():

    if os.path.isfile('slater.dat'):
        data = np.loadtxt('slater.dat')
    else:
        raise RuntimeError('slater.dat was not found, run brute_slater_hellium() first')

    import matplotlib.pyplot as plt
    fig,ax = plt.subplots(1,1)
    ax.set_xlabel('Slater orbital exponent (bohr$^{-1}$)',fontsize=16)
    ax.set_ylabel('VMC energy (ha)',fontsize=16)

    myx = data[:,0] # parameters
    myy = data[:,1] # VMC energies
    myye= data[:,2] # VMC energy errors
    lines = ax.errorbar(myx,myy,yerr=myye,fmt='')
    plt.show()

def linear():
    wf = ExponentSlaterWF()
    # get psi_i/psi_0
    # get S_ij
    # get H_ij

if __name__ == '__main__':
    brute_slater_hellium()
    plot_slater_hellium()
# end __main__
