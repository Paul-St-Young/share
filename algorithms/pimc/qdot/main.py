#!/usr/bin/env python
import numpy as np
from path import Path
from input_manager import InputManager
from col import corr,error

def harmonic(conf,lam,omega):
    """ conf has shape: (nptcl,ndim) """
    return omega*omega/(4.*lam) * (np.linalg.norm(conf,axis=1)**2.).sum()

if __name__ == '__main__':

    # parse inputs
    inp_manager = InputManager()
    args = inp_manager.parse_command_line()
    #cmd_inp = vars(args) # this is the proper way
    globals().update(vars(args)) # this is a BAD idea, but quick and dirty
    tau = beta/nslice

    # initialize path
    path = Path(tau,lam=lam,nslice=nslice,nptcl=nptcl,ndim=ndim)
    path.set_ext_potential(lambda x:harmonic(x,lam,omega)) 
    path.set_int_potential()
    old_action = path.action(from_scratch=True)

    x2 = np.zeros(nsample)
    #path_trace = np.zeros([nsample,nslice,nptcl,ndim])
    nmove = 0
    naccept = 0
    for isample in range(nsample):
        # collect statistics
        #path_trace[isample] = path.confs
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
    #np.savetxt('x2.dat',x2)
    #np.savetxt('pos.dat',path_trace)

    accept = float(naccept)/nmove
    x2eq = x2[nequil:]
    fmt  = "{omega:6.2f}  {beta:4.2f}  {sig:4.2f}  {accept:3.2f}  {corr:3.1f}  {x2:4.6f}  {x2e:4.6f}"
    output = fmt.format(
        omega = omega,
        beta  = beta,
        sig   = sig,
        accept= accept,
        corr  = corr(x2eq),
        x2    = np.mean(x2eq),
        x2e   = error(x2eq)
    )
    print output

# end __main_
