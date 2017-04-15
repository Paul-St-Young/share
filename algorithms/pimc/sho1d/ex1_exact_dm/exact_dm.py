#!/usr/bin/env python
# PIMC Tutorial: Part 1 exact SHO DM
# Author: Yubo "Paul" Yang
# Date: Apr. 13 2017
# Last Modified: Apr. 15 2017
from __future__ import print_function
import numpy as np
from stats import corr,error

opt_sig = lambda omega,beta,lam:np.sqrt( -1./( 2.*ln_rho(1.,omega,beta,lam) ) )

def ln_rho(x,omega,beta,lam):
    """ exponent of linear harmonic oscillator density matrix:
         potential V(x) = 0.5*omega**2.*x**2
        mass is set to 1. implicitly """
    ratio = omega/(4*lam*np.sinh(beta*omega))
    const = -0.5*np.log( ratio/np.pi )
    exp   = -2.*x*x*(np.cosh(beta*omega)-1)
    return ratio*exp + const
# en def 

def sample_1d_harmonic_analytic(ln_rho,omega,beta,lam,sig,block_size):
    """ calculate <x^2> using analytic density matrix of a linear oscillator with unit mass
     ln_rho: analytic expression for the density matrix exponent
     omega:  oscillator frequency
     beta:   inverse temperature
     sig:    step size used to sample the density matrix
    return: acceptance rate, trace of <x^2>
    """
    naccept = 0
    oldx = 0.0
    x2  = np.zeros(nsample)
    for isample in range(nsample):
        x2[isample]  = oldx*oldx
        for istep in range(block_size):
            newx = oldx+np.random.randn()*sig
            #newx = np.random.randn()*sig # !!! misleading !!! uncorrelated samples before equilibration
            prob = np.exp( ln_rho(newx,omega,beta,lam) - ln_rho(oldx,omega,beta,lam) )
            if np.random.rand() < prob:
                oldx = newx
                naccept += 1
            # end if
        # end for
    # end for isample
    return float(naccept)/nsample/block_size,x2
# end def

def parse_inputs():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-o','--omega',type=float,default=10.0,help='spring freq.')
    parser.add_argument('-b','--beta',type=float,default=1.0,help='inverse temp.')
    parser.add_argument('-l','--lam',type=float,default=0.5,help='1/(2*mass)')
    parser.add_argument('-s','--sig',type=float,default=0.5,help='step size')
    parser.add_argument('-bs','--block_size',type=int,default=5,help='steps per block to remove autocorrelation')
    parser.add_argument('-neq','--nequil',type=int,default=0,help='number of equilibration steps')
    parser.add_argument('-n','--nsample',type=int,default=100,help='number of samples to collect')
    parser.add_argument('-opt','--use_opt_sig',action='store_true',help='use optimal sigma')
    args = parser.parse_args()

    return args.omega, args.beta, args.lam, args.sig, args.nequil, args.nsample, args.use_opt_sig, args.block_size
# end def

if __name__ == '__main__':

    omega,beta,lam,sig,nequil,nsample,use_opt_sig,block_size = parse_inputs()
    # calculate optimal step size
    if use_opt_sig:
        sig = opt_sig(omega,beta,lam)
    # end if

    accept,x2 = sample_1d_harmonic_analytic(ln_rho,omega,beta,lam,sig,block_size)

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
    print( output )
    #print( omega,beta,sig,accept,corr(x2eq),np.mean(x2eq),error(x2eq) )
    np.savetxt('ax2.dat',x2)
# end __main__
