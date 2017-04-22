#!/usr/bin/env python
import numpy as np
from copy import deepcopy
from path import Path
from input_manager import InputManager

def harmonic(x,lam,omega):
    return omega*omega*x*x/(4.*lam)

if __name__ == '__main__':

    # parse inputs
    inp_manager = InputManager()
    cmd_inp = inp_manager.parse_command_line()
    args = inp_manager.parse_command_line()
    # print vars(args) # see what variables have been read
    globals().update(vars(args))
    tau = beta/nslice

    # initialize path
    path = Path( tau,lam=lam,nslice=nslice,nptcl=nptcl,ndim=ndim)
    path.set_ext_potential(lambda x:harmonic(x,lam,omega)) 
    path.set_int_potential()
    old_action = path.action(from_scratch=True)

    x2 = np.zeros(nsample)
    path_trace = np.zeros([nsample,nslice,nptcl,ndim])
    nmove = 0
    naccept = 0
    for isample in range(nsample):
        # collect statistics
        path_trace[isample] = path.confs
        x2[isample] = (np.linalg.norm(path.confs,axis=1)**2.).mean()
        for istep in range(block_size):
            # single bead moves
            for iconf in range(nslice):
                move = sig*np.random.randn(nptcl,ndim)
                path.move_conf(iconf,move)
                nmove += 1
                new_action = path.action(from_scratch=False)
                prob = np.exp(-(new_action-old_action))
                if np.random.rand()<prob:
                    naccept += 1
                    old_action = new_action
                else:
                    path.move_conf(iconf,-move)
                # end if
            # end for iconf
        # end for istep
    # end for isample
    np.savetxt('x2.dat',x2)
    np.savetxt('pos.dat',path_trace)
    print float(naccept)/nmove

# end __main__
