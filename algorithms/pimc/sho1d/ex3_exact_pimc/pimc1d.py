#!/usr/bin/env python
# PIM Tutorial: Part 3 PIMC SHO 
# Author: Yubo "Paul" Yang
# Date: Apr. 14 2017
from __future__ import print_function
import numpy as np
from exact_dm import parse_inputs,opt_sig
from exact_link import action
from stats import corr,error

if __name__ == '__main__':

    omega,beta,lam,sig,nequil,nsample,use_opt_sig,block_size = parse_inputs()
    # calculate optimal step size
    if use_opt_sig:
        sig = opt_sig(omega,beta,lam)
    # end if

    # extra simulation inputs
    nslice = 10
    tau = beta/nslice
    sig1 = opt_sig(omega,tau,lam)

    path = sig*np.random.randn(nslice)
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

            # single-bead moves
            # ---- 
            for islice in range(nslice):

                old_action = action(path,omega,beta,lam)

                # single bead move
                move = sig1*np.random.randn()
                path[islice] += move

                # calculate action change
                new_action = action(path,omega,beta,lam)

                # accept or recject
                prob = np.exp(-(new_action-old_action)) # action = -ln_rho
                if np.random.rand() < prob:
                    naccept += 1
                else:
                    path[islice] -= move
                # end if prob
                nmove += 1
            # end for islice

        # end for istep
    # end for isample

    np.savetxt('pos.dat',pos)
    np.savetxt('x2.dat',x2)
    #pos2 = pos[nequil:]*pos[nequil:]
    x2eq = x2[nequil:]
    accept = float(naccept)/nmove #float(naccept)/nsample/nslice/block_size/2.
    print( omega,beta,sig,accept,corr(x2eq),np.mean(x2eq),error(x2eq) )

# end __main__

