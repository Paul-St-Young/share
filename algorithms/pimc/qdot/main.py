#!/usr/bin/env python
import numpy as np
from copy import deepcopy
from path import Path

def harmonic(x):
    lam   = 0.5
    omega = 5.0
    return omega*omega*x*x/(4.*lam)

if __name__ == '__main__':

    tau = 0.5
    sig = 0.02
    nslice = 10
    nptcl  = 1
    ndim   = 1
    path = Path( tau,lam=0.5,nslice=nslice,nptcl=nptcl,ndim=ndim)
            #,confs=np.array([ [[-0.2]] , [[0.2]] ]) )
    path.set_ext_potential(harmonic) 
    path.set_int_potential()
    old_action = path.action(from_scratch=True)

    cur = 0 # current configuration (~cur points to the proposed configuration)
    mc_pair = [path,deepcopy(path)]

    nsample = 1000 # number of samples to gather
    block_size = 10 # no blocking
    x2 = np.zeros(nsample)
    path_trace = np.zeros([nsample,nslice,nptcl,ndim])
    nmove = 0
    naccept = 0
    for isample in range(nsample):
        # collect statistics
        path_trace[isample] = mc_pair[cur].confs
        x2[isample] = np.linalg.norm(mc_pair[cur].confs,axis=1).mean()
        for istep in range(block_size):
            # single bead moves
            for iconf in range(nslice):
                mc_pair[~cur].move_conf(iconf,sig*np.random.randn(nptcl,ndim))
                nmove += 1
                new_action = mc_pair[~cur].action(from_scratch=False)
                prob = np.exp(-(new_action-old_action))
                if np.random.rand()<prob:
                    naccept += 1
                    cur = ~cur
                    old_action = new_action
                # end if
            # end for iconf
        # end for istep
    # end for isample
    np.savetxt('x2.dat',x2)
    np.savetxt('paths.dat',path_trace)
    print float(naccept)/nmove

# end __main__
