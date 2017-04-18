#!/usr/bin/env python
# PIM Tutorial: Part 3 PIMC SHO 
# Author: Yubo "Paul" Yang
# Date: Apr. 14 2017
from __future__ import print_function
import numpy as np
from exact_dm import parse_inputs,opt_sig
from pidm import primitive_link_action
from stats import corr,error

def action(path,omega,beta,lam):
    nslice = len(path)
    tau    = beta/nslice
    tot    = 0.0
    for islice in range(nslice):
        tot += primitive_link_action(path[islice],path[(islice+1)%nslice],
            omega,tau,lam)
    return tot

if __name__ == '__main__':

    omega,beta,lam,sig,nequil,nsample,use_opt_sig,block_size = parse_inputs()

    # extra simulation inputs
    nslice = 20
    tau = beta/nslice

    # calculate optimal step size
    if use_opt_sig:
        sig = opt_sig(omega,beta,lam)
    # end if

    path = 0.1*np.random.randn(nslice)
    naccept = 0
    nmove   = 0
    pos = np.zeros(nsample)
    x2  = np.zeros(nsample)
    for isample in range(nsample):
        pos[isample] = path.mean()
        x2[isample]  = (path**2.).mean()
        for istep in range(block_size):
            # displacement move
            # ---- 
            old_action = action(path,omega,beta,lam)
            disp = sig*np.random.randn()
            path += disp
            new_action = action(path,omega,beta,lam)
            # accept or recject
            prob = np.exp(-(new_action-old_action)) # action = -ln_rho
            if np.random.rand() < prob:
                naccept += 1
            else:
                path -= disp
            # end if prob
            nmove += 1

            for islice in range(nslice):

                old_action = action(path,omega,beta,lam)
                old_x0 = path[islice]
                old_x1 = path[(islice+1)%nslice]

                # single bead move
                new_x0 = old_x0
                new_x1 = old_x1 + np.random.randn()*opt_sig(omega,tau,lam)
                path[islice] = new_x0
                path[(islice+1)%nslice] = new_x1

                # calculate action change
                new_action = action(path,omega,beta,lam)
                prob = np.exp(-(new_action-old_action)) # action = -ln_rho

                # accept or recject
                if np.random.rand() < prob:
                    naccept += 1
                else:
                    path[islice] = old_x0
                    path[(islice+1)%nslice] = old_x1
                # end if prob
                nmove += 1
            # end for islice
        # end for istep
    # end for isample

    np.savetxt('pos.dat',pos)
    pos2 = pos[nequil:]*pos[nequil:]
    x2eq = x2[nequil:]
    accept = float(naccept)/nmove #float(naccept)/nsample/nslice/block_size
    print( omega,beta,sig,accept,corr(pos2),np.mean(x2eq),error(x2eq) )

# end __main__

