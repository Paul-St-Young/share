#!/usr/bin/env python
# PIMC Tutorial: Part 4 Primitive Action
# Author: Yubo "Paul" Yang
# Date: Apr. 13 2017
# Last Modified: Apr. 15 2017
import numpy as np
def kinetic_action(x0,x1,lam,tau):
    return (x0-x1)**2./(4.*lam*tau)+1./2*np.log(4*np.pi*lam*tau)
def potential_action(x0,x1,omega,lam,tau):
    omega2 = omega*omega
    pot1   = omega2*x0*x0/(4.*lam)
    pot2   = omega2*x1*x1/(4.*lam)
    return 0.5*tau*(pot1+pot2)
def primitive_link_action(x0,x1,omega,tau,lam):
    return kinetic_action(x0,x1,lam,tau) + potential_action(x0,x1,omega,lam,tau)

def exact_action(x0,x1,lam,omega,beta):
    ratio = omega/(4*lam*np.sinh(beta*omega))
    const = -0.5*np.log( ratio/np.pi )
    exp   = (x0*x0+x1*x1)*np.cosh(beta*omega) - 2*x0*x1
    return ratio*exp + const

def show_actions(ax,myx,x1,lam,omega):
    colors = ['k','b','y','pink','r']
    itau = 0
    for tau in [5.0,1.0,0.5,0.1,0.01]:
        color = colors[itau]
        myy = primitive_link_action(myx,x1,omega,tau,lam)
        myy0= exact_action(myx,x1,lam,omega,tau)

        line0 = ax.plot(myx,myy0,c=color,label=r'$\tau$=%3.2f'%tau)
        line  = ax.plot(myx,myy,'--',c=color,lw=2)
        itau += 1
    # end for
    return line0,line
# end def

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    lam   = 0.5
    omega = 1.0
    
    x1  = 0.0
    myx = np.linspace(-1,1,100)

    fig,ax = plt.subplots(1,1)
    ax.set_xlabel(r'x',fontsize=20)
    ax.set_ylabel(r'$\rho(x,0,\tau)$',fontsize=20)
    line0,line = show_actions(ax,myx,x1,lam,omega)
    ax.set_ylim(-2,10)
    leg = ax.legend()
    ax.add_artist(leg)
    leg1 = ax.legend(handles=[line0[0],line[0]]
        ,labels=['exact','primitive'],loc='upper left')
    ax.annotate(xy=(-0.9,-1),s=r'$\omega$=%3.2f'%omega,fontsize=16)

    ax1 = fig.add_axes([0.43,0.58,0.2,0.3])
    myx = np.linspace(-0.2,0.2,100)
    line0,line = show_actions(ax1,myx,x1,lam,omega)
    ax1.set_ylim(-0.3,1.2)
    ax1.set_xlim(-0.21,0.21)
    ax1.set_xticks([-0.2,0,0.2])
    plt.show()
