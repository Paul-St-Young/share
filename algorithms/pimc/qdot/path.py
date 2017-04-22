import numpy as np

class Path:

    def __init__(self,tau,lam=0.5,nslice=1,nptcl=1,ndim=1,confs=None):
        self._lam = lam
        self._tau = tau
        self._nslice = nslice
        self._nptcl  = nptcl
        self._ndim   = ndim

        self.confs = np.zeros([nslice,nptcl,ndim])
        if confs is not None:
            if self.confs.shape != confs.shape:
                raise RuntimeError('given path has wrong shape %s, expected nslice,nptcl,ndim=%s' % (confs.shape,self.confs.shape) )
            # end if
            self.confs = confs.copy()
        # end if
        self._alinks = np.zeros(nslice) # link action alink[i] = S(i,i+1;tau)
        self._klinks = np.zeros(nslice) # kinetic contr. to link action
        self._pconfs = np.zeros(nslice) # potential of every slice

        self._update_alinks = True

    def __str__(self):
        return str(self.confs)

    # give path access to potential
    def _validate_potential_function(self,function):
        return_val = function(self.confs[0])
        allowed_types = set([float,np.float64,np.float32])
        if type(return_val) not in allowed_types:
            raise RuntimeError( "potential function must return float when applied to a configuration, got type(%s) = %s instead" % (return_val,type(return_val)) )
        # end if
    def set_ext_potential(self,function=None):
        self.ex_pot = function
        if function is None:
            self.ex_pot = lambda x:0.0 # free particle
        self._validate_potential_function(self.ex_pot)
    def set_int_potential(self,function=None):
        self.int_pot = function
        if function is None:
            self.int_pot = lambda x:0.0 # free particle
        self._validate_potential_function(self.int_pot)

    # give path access to kinetic
    def kinetic_alink(self,iconf): # _klinks[iconf] links iconf-1 -> iconf
        iprev = (iconf-1)%self._nslice
        dx2 = np.linalg.norm(self.confs[iprev]-self.confs[iconf],axis=1)**2.
        return dx2.sum()/(4.*self._lam*self._tau)

    def update_alinks(self):
        """ renew link actions from kinetic link actions and potential of every time slice """
        self._alinks = self._klinks + 0.5*self._tau*(
                self._pconfs+np.append(self._pconfs[1:],self._pconfs[0])
        )

    def action(self,from_scratch=False):
        """ update link actions if needed, then return sum of link actions """
        if from_scratch:
            for iconf in range(self._nslice):
                self.request_potential(iconf)
                self.request_kinetic_link(iconf)
        if self._update_alinks:
            self.update_alinks()
            self._update_alinks = False
        return self._alinks.sum()

    def move_conf(self,iconf,move):
        legal_shape = self.confs[0].shape
        if move.shape != legal_shape:
            raise RuntimeError('illegal move of shape %s, expect %s'%(move.shape,legal_shape))
        self.confs[iconf] += move
        self.request_potential(iconf)
        self.request_kinetic_link(iconf)

    def request_potential(self,iconf):
        """ ask for potential of configuration iconf to be calculated """
        self._update_alinks = True # tell action to update

        # code request object later, for now handle request locally
        self._pconfs[iconf] = self.ex_pot(self.confs[iconf]) + self.int_pot(self.confs[iconf])

    def request_kinetic_link(self,iconf): 
        """ ask for kinetic link action between iconf-1&iconf, iconf&iconf+1 to be calculated  """
        self._update_alinks = True

        # code request object later, for now handle request locally
        self._klinks[iconf] = self.kinetic_alink(iconf)
        inext = (iconf+1)%self._nslice
        self._klinks[inext] = self.kinetic_alink(inext)

# end class Path

if __name__ == '__main__':

    # test action
    path = Path( 0.1,lam=0.5,nslice=2,nptcl=1,ndim=1
        ,confs=np.array([ [[1]] , [[2]] ]) )
    path.set_ext_potential(lambda x:0.5*(np.linalg.norm(x,axis=1)**2.).sum())
    path.set_int_potential()
    assert np.isclose( path.action(from_scratch=True),10.25 ), 'failed action test'

    # test action change
    path = Path( 0.1,lam=0.5,nslice=2,nptcl=3,ndim=2
        ,confs=np.array([ [[0,0],[0,1],[0,2]] , [[1,0],[-1,1],[0.5,0.5]] ]) )
    path.set_ext_potential(lambda x:0.5*(np.linalg.norm(x,axis=1)**2.).sum())
    path.set_int_potential()
    old_action = path.action(from_scratch=True)
    path.move_conf(0,np.random.randn(3,2))
    new_action = path.action(from_scratch=False)
    true_action= path.action(from_scratch=True)
    assert np.isclose(new_action,true_action), 'failed action change test'

