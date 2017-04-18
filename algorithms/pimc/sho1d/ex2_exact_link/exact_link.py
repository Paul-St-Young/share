#!/usr/bin/env python
# PIMC Tutorial: Part 2 exact link action
# Author: Yubo "Paul" Yang
# Date: Apr. 14 2017
# Last Modified: Apr. 15 2017
from __future__ import print_function
import numpy as np
from exact_dm import parse_inputs,ln_rho,opt_sig
from stats import corr,error

def exact_link_action(x0,x1,omega,beta,lam):
    """ action = -ln(density matrix)
     link action is -ln(rho(x0,x1,beta)), because it links bead x0 to x1 """
    ratio = omega/(4*lam*np.sinh(beta*omega))
    const = -0.5*np.log( ratio/np.pi )
    exp   = (x0*x0+x1*x1)*np.cosh(beta*omega) - 2*x0*x1
    return ratio*exp + const

def action(path,omega,beta,lam):
    """ total action of a closed path """
    nslice = len(path)
    tau    = beta/nslice
    tot     = 0.0
    for islice in range(nslice):
        tot += exact_link_action(path[islice],path[(islice+1)%nslice],
            omega,tau,lam)
    return tot

def classical_path(x,omega,beta,nslice):
    """ classical path of a 1d sho in imaginary time constraint to 
     boundary condition of beginning and ending at x at 
     imaginary times 0 and beta """
    path0 = np.zeros(nslice)
    tau = beta/nslice
    for islice in range(nslice):
        t = tau*islice
        sinh_piece = (1-np.cosh(omega*beta))*np.sinh(omega*t)/np.sinh(omega*beta)
        cosh_piece = np.cosh(omega*t)
        path0[islice] = x*(sinh_piece + cosh_piece)
    # end for islice
    return path0

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    omega,beta,lam,sig,nequil,nsample,use_opt_sig,block_size = parse_inputs()

    """ # check that exact_link_action can reproduce -ln_rho
    check_link = lambda x,omega,beta,lam:exact_link_action(x,x,omega,beta,lam)
    finex = np.linspace(-1,1,10)
    plt.plot(finex,check_link(finex,omega,beta,lam))
    plt.plot(finex,-ln_rho(finex,omega,beta,lam),ls='--',c='k',lw=2)
    plt.show()
    """

    # extra simulation inputs
    nslice = 10
    tau = beta/nslice

    # calculate optimal step size
    if use_opt_sig:
        sig = opt_sig(omega,beta,lam)
    # end if
    sig1 = opt_sig(omega,tau,lam) # single bead step size

    # initialize a random path, calculate exact DM diagonal
    path    = sig*np.random.randn(nslice)
    action0 = -ln_rho(path[0],omega,beta,lam)
    path0   = classical_path(path[0],omega,beta,nslice)

    action_arr = np.zeros(nsample) # integrate over links to get action from convolution
    old_action = action(path,omega,beta,lam)
    new_action = 0.0
    naccept = 0
    all_paths = np.zeros([nslice,nsample])
    for isample in range(nsample):
        all_paths[:,isample] = path
        action_arr[isample] = old_action
        for istep in range(block_size):
            for islice in range(1,nslice):
                move = sig1*np.random.randn()
                path[islice] += move
                new_action = action(path,omega,beta,lam)
                prob = np.exp(-(new_action-old_action))

                if np.random.rand() < prob:
                    naccept += 1
                    old_action = new_action
                else:
                    path[islice] -= move
                # end if
            # end for islice
        # end for istep
    # end for isample
    print( float(naccept)/nsample/block_size/(nslice-1) )
    np.savetxt('action.dat',action_arr)
    acteq = action_arr[nequil:]
    act_mean = np.mean(acteq)
    act_error= error(acteq)

    path_mean= np.mean(all_paths,axis=1)
    path_sig = np.std(all_paths,axis=1)
    fig,ax = plt.subplots(1,1)
    ax.set_xlabel('x',fontsize=16)
    ax.set_ylabel('t',fontsize=16)
    ax.errorbar(path_mean,tau*np.arange(nslice)
        ,xerr=path_sig/np.sqrt(nsample-nequil)
        ,fmt='.-',label='sampled path')
    ax.plot(path0,tau*np.arange(nslice),c='k',label='classical path')
    #ax.annotate(xy=(-0.5,3),s='true=%3.2f'%action0)
    #ax.annotate(xy=(0.5,3),s='link=%3.2f+-%3.2f'%(act_mean,act_error))
    print(action0,act_mean,'+-',act_error)
    ax.set_xlim(-1,1)
    ax.legend()
    #fig.savefig('classical_path.png',dpi=200)
    plt.show()

# end __main__
