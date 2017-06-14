#!/usr/bin/env python
#This is not the most efficient (in memory or computer time) implementation. 
#It is supposed to be relatively straightforward to 
#understand and flexible enough to play with.
#We will have to decide how much we want to give them 
#(the structure, library functions, etc), 
#and how much we want to have them develop.
import numpy as np
import wavefunction

#####################################

class Hamiltonian:
  def __init__(self,Z=2):
    self.Z=Z
    pass
  def pot_en(self,pos):
    """ electron-nuclear potential of configurations 'pos' """
    r=np.sqrt(np.sum(pos**2,axis=1))
    return np.sum(-self.Z/r,axis=0)
  def pot_ee(self,pos):
    """ electron-electron potential of configurations 'pos' """
    ree=np.sqrt(np.sum((pos[0,:,:]-pos[1,:,:])**2,axis=0))
    return 1/ree
  def pot(self,pos):
    """ potential energy of configuations 'pos' """
    return self.pot_en(pos)+self.pot_ee(pos)

#####################################

def drift_vector(pos,wf,tau=None,scaled=False):
    """ calculate the drift vector for importance sampling
    Input:
       pos: 3D numpy array of electron positions (nelec,ndim,nconf)
       wf:  wavefunction to be sampled (i.e. psi)
    Return: 
       dvec: drift vector needed for electrons to importance sample psi^2
    """

    # drift vector = (\nabla^2\ln\psi^2)/(2m) = grad_psi_over_psi
    dvec= wf.gradient(pos) 
    if scaled: # rescale drift vector to limit its magnitude near psi=0
        if tau is None:
            raise RuntimeError('time step must be given to calculate scaled drift')
        vec_sq = np.sum(dvec**2.,axis=1)
        # Umrigar, JCP 99, 2865 (1993).
        vscale  = (-1.+np.sqrt(1+2*vec_sq*tau))/(vec_sq*tau)
        dvec   *= vscale[:,np.newaxis,:]
    return dvec

def drift_prob(posold,posnew,gauss_move_old,driftnew,tau):
    """ return the ratio of forward and backfward move probabilities for rejection algorith,
    Input:
      posold: electron positions before move (nelec,ndim,nconf) 
      posnew: electron positions after  move (nelec,ndim,nconf)
      gauss_move_old: randn() numbers for forward move
      driftnew: drift vector at posnew 
      tau: time step
    Return:
      ratio: [backward move prob.]/[forward move prob.]
      """

    # randn numbers needed for backward move
    gauss_move_new = (posold-posnew-tau*driftnew)/np.sqrt(tau)
    # assume the following drift-diffusion move
    #assert np.allclose( posold,posnew+np.sqrt(tau)*gauss_move_new+tau*driftnew ) 

    # calculate move probabilities
    gauss_old_sq = np.sum( np.sum(gauss_move_old**2.,axis=1) ,axis=0)
    gauss_new_sq = np.sum( np.sum(gauss_move_new**2.,axis=1), axis=0)
    forward_green  = np.exp(-gauss_old_sq/2.)
    backward_green = np.exp(-gauss_new_sq/2.)

    ratio = backward_green/forward_green
    return ratio

#####################################

def metropolis_sample(pos,wf,tau=0.01,nstep=1000,use_drift=False):
  """
  Input variables:
    pos: a 3D numpy array with indices (electron,[x,y,z],configuration ) 
    wf: a Wavefunction object with value(), gradient(), and laplacian()
  Returns: 
    posnew: A 3D numpy array of configurations the same shape as pos, distributed according to psi^2
    acceptance ratio: 
  """

  # initialize
  posnew = pos.copy()
  posold = pos.copy()
  wfold  = wf.value(posold)
  if use_drift:
    driftold = drift_vector(posold,wf,tau=tau,scaled=True)
  acceptance=0.0
  nconf=pos.shape[2]
  for istep in range(nstep):

    # propose a move
    gauss_move_old = np.random.randn(*posold.shape)
    posnew=posold+np.sqrt(tau)*gauss_move_old
    if use_drift:
        posnew += tau*driftold

    wfnew=wf.value(posnew)

    # calculate Metropolis-Rosenbluth-Teller acceptance probability
    #  VMC uses rejection to sample psi_sq by maintaining detailed balance
    prob = wfnew**2/wfold**2 # for reversible moves
    if use_drift: # multiply ratio of probabilities of backward/forward moves
        driftnew = drift_vector(posnew,wf,tau=tau,scaled=True)
        prob *= drift_prob(posold,posnew,gauss_move_old,driftnew,tau)

    # get indices of accepted moves
    acc_idx = (prob + np.random.random_sample(nconf) > 1.0)

    # update stale stored values for accepted configurations
    posold[:,:,acc_idx] = posnew[:,:,acc_idx]
    if use_drift:
        driftold[:,:,acc_idx] = driftnew[:,:,acc_idx]
    wfold[acc_idx] = wfnew[acc_idx]
    acceptance += np.mean(acc_idx)/nstep

  return posold,acceptance

#####################################

def local_energy(pos,wf,ham):
  return -0.5*np.sum(wf.laplacian(pos),axis=0)+ham.pot(pos)

#####################################

def test_cusp():
  import matplotlib.pyplot as plt

  wf=wavefunction.JastrowWF(1.0)
  ham=Hamiltonian()

  # make sure jastrow has the right cusp
  assert(np.isclose(wf.Z,ham.Z))
  smallshift=1e-7
  path=np.zeros((2,3,1,100))+smallshift
  path[0,0,:,:]=np.linspace(-0.5,1,100)[np.newaxis,np.newaxis,:]
  path[1,0,:,:]=0.5+smallshift

  nuc_energy=ham.pot_en(path)
  elec_energy=ham.pot_ee(path)
  kin_energy=-0.5*np.sum(wf.laplacian(path),axis=0)
  tot_energy=kin_energy+nuc_energy+elec_energy

  fig,ax=plt.subplots(1,1)
  ax.plot(path[0,0,0,:],kin_energy[0],label='kinetic')
  ax.plot(path[0,0,0,:],nuc_energy[0],label='nuclear')
  ax.plot(path[0,0,0,:],elec_energy[0],label='interaction')
  ax.plot(path[0,0,0,:],tot_energy[0],label='total')
  ax.legend(loc='upper left',bbox_to_anchor=(1.0,1.0),frameon=False)

  ax.set_ylim((-100,100))
  ax.set_xlabel('x-coordinate')
  ax.set_ylabel('Energy (Ha)')
  fig.set_size_inches(5,3)
  fig.tight_layout()
  fig.subplots_adjust(right=0.60)
  fig.savefig('cusp_test.pdf')

#####################################

def test_vmc(
    nconfig=1000, ndim=3,
    nelec=2,
    nstep=100,
    tau=0.5,
    wf=wavefunction.ExponentSlaterWF(alpha=1.0),
    ham=Hamiltonian(Z=1),
    use_drift=False
    ):
  ''' Calculate VMC energies and compare to reference values.'''

  print( 'VMC test: 2 non-interacting electrons around a fixed proton' )

  # initialize electrons randomly
  possample     = np.random.randn(nelec,ndim,nconfig)
  # sample exact wave function
  possample,acc = metropolis_sample(possample,wf,tau=tau,nstep=nstep,use_drift=use_drift)

  # calculate kinetic energy
  ke   = -0.5*np.sum(wf.laplacian(possample),axis=0)
  # calculate potential energy
  vion = ham.pot_en(possample)
  eloc = ke+vion

  # report
  print( "Cycle finished; acceptance = {acc:3.2f}.".format(acc=acc) )
  for nm,quant,ref in zip(['kinetic','Electron-nucleus','total']
                         ,[ ke,       vion,              eloc]
                         ,[ 1.0,      -2.0,              -1.0]):
    avg=np.mean(quant)
    err=np.std(quant)/np.sqrt(nconfig)
    print( "{name:20s} = {avg:10.6f} +- {err:8.6f}; reference = {ref:5.2f}".format(
      name=nm, avg=avg, err=err, ref=ref) )

#####################################

def test_hellium(
    nconfig=1000, ndim=3,
    nelec=2,
    nstep=100,
    tau=0.5,
    wf=wavefunction.ExponentSlaterWF(alpha=1.0),
    ham=Hamiltonian(Z=2),
    use_drift=False
    ):
  ''' Calculate VMC energies and compare to reference values.'''

  print( 'VMC test: Hellium ground state' )

  # initialize electrons randomly
  possample     = np.random.randn(nelec,ndim,nconfig)
  # sample trial wave function
  possample,acc = metropolis_sample(possample,wf,tau=tau,nstep=nstep,use_drift=use_drift)

  # calculate kinetic energy
  ke   = -0.5*np.sum(wf.laplacian(possample),axis=0)
  # calculate potential energy
  pot  = ham.pot(possample)
  eloc = ke+pot

  # report
  print( "Cycle finished; acceptance = {acc:3.2f}.".format(acc=acc) )
  for nm,quant,ref in zip(['kinetic','potential','total']
                         ,[ ke,       pot,        eloc]
                         ,[ 2.848, -5.696,      -2.848]):
    avg=np.mean(quant)
    err=np.std(quant)/np.sqrt(nconfig)
    print( "{name:20s} = {avg:10.6f} +- {err:8.6f}; reference = {ref:5.2f}".format(
      name=nm, avg=avg, err=err, ref=ref) )
  return avg,err
#####################################

if __name__=="__main__":
  test_cusp()
  test_vmc(use_drift=False)
  test_vmc(use_drift=True)
  test_hellium(tau=0.4,use_drift=True,wf=wavefunction.JastrowWF(1e9))
