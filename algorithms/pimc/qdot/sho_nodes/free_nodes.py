#!/usr/bin/env python
import numpy as np
from path import Path

def exact_sho_dm(conf1,conf2,omega,beta,lam):
    nptcl = len(conf1)
    rho_mat = np.zeros([nptcl,nptcl])
    for i in range(nptcl):
        for j in range(nptcl):
            rho_mat[i,j] = exact_sho_1dm(conf1[i],conf2[j],omega,beta,lam)
        # end for j
    # end for i
    return np.linalg.det(rho_mat)

def exact_sho_1dm(r1,r2,omega,beta,lam):
    """  exact one-body density matrix of a harmonic oscillator
     r1,r2 have shape (ndim) """
    ratio = omega/(4.*lam*np.sinh(beta*omega))
    r1sq  = np.dot(r1,r1)
    r2sq  = np.dot(r2,r2)
    r12   = np.dot(r1,r2)
    expo  = (r1sq+r2sq)*np.cosh(beta*omega) - 2.*r12
    return np.exp(-ratio*expo)

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-beta',type=float,default=5.0,help='inverse temperature, default 5.0')
    args = parser.parse_args()

    nslice= 2
    nptcl = 3 
    ndim  = 2

    conf1 = np.array(
        [ [-1.3,1.8],[-0.2,1.6],[2.8,1.4] ]
    )
    conf2 = conf1.copy()
    conf2[2,1] = 0.1

    beta = args.beta
    path = Path(beta,nslice=nslice,nptcl=nptcl,ndim=ndim
            ,confs=np.array([conf1,conf2]))

    nx  = 25
    myx = np.linspace(-3,3,nx)
    myy = np.linspace(-3,3,nx)

    my_rho = np.zeros([nx,nx])
    exact_rho = np.zeros([nx,nx])
    for i in range(nx):
        for j in range(nx):
            path.confs[1,2,0] = myx[i]
            path.confs[1,2,1] = myy[j]
            try:
                val = path.kinetic_action(0,1)
                my_rho[i,j] = 1
            except RuntimeError:
                my_rho[i,j] = -1

            true_dm = exact_sho_dm(path.confs[0],path.confs[1],1.0,beta,0.5)
            if true_dm > 0:
                exact_rho[i,j] = 1
            else:
                exact_rho[i,j] = -1
        # end for i
    # end for j
    
    import matplotlib.pyplot as plt
    fig,ax = plt.subplots(1,1)
    ax.plot(conf1.T[0],conf1.T[1],'o')
    ax.contour(myx,myy,my_rho.T,label='free')
    ax.contour(myx,myy,exact_rho.T,label='exact')
    plt.show()
