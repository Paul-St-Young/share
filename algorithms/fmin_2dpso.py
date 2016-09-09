import numpy as np
from copy import deepcopy

class PSOMin2D:
    
    def __init__(self,landscape,xmin,xmax,max_hop,pop_size=10,c1=2,c2=2):
        
        # save parameters
        # !!!! hard-code 2D
        self.ndim = 2
        self.max_hop = max_hop
        self.c1 = c1
        self.c2 = c2
        self.xmin = xmin
        self.xmax = xmax
        
        # register model
        self.landscape = landscape
        
        # initialize population
        self.pop = (xmax-xmin) * np.random.rand(pop_size,self.ndim) + xmin
        
        # initialize individual best
        self.individual_best     = np.apply_along_axis(landscape,1,self.pop)
        self.individual_best_pos = deepcopy(self.pop)

        # find global best
        min_idx              = np.argmin(self.individual_best)
        self.global_best     = self.individual_best[min_idx].copy()
        self.global_best_pos = self.pop[min_idx].copy()
        
        # initialize hopping sizes and directions
        self.hop = max_hop * np.random.rand(pop_size,self.ndim)
    # end def
    
    def run_nsteps(self,max_it):
        # keep a trace of global best
        global_best_trace = np.zeros(max_it+1)
        for istep in range(max_it):
    
            # keep trace
            global_best_trace[istep] = self.global_best

            # evaluate fitness of population
            fitness = np.apply_along_axis(self.landscape,1,self.pop)

            # update global best
            min_idx      = np.argmin(fitness)
            current_best = fitness[min_idx]
            if current_best < self.global_best:
                self.global_best     = current_best
                self.global_best_pos = self.pop[min_idx].copy()
            # end if

            # update individual best
            idx = np.where( np.array(fitness) < np.array(self.individual_best) )
            self.individual_best[idx]     = fitness[idx]
            self.individual_best_pos[idx] = deepcopy( self.pop[idx] )

            # update hopping
            self.hop += self.c1*np.random.rand()*(self.individual_best_pos-self.pop) +\
                        self.c2*np.random.rand()*(self.global_best_pos-self.pop)
            idx = np.where( abs(self.hop) > self.max_hop )
            self.hop[idx] = np.sign(self.hop[idx])*self.max_hop

            # update populaton
            self.pop += self.hop

        # end for istep
        
        global_best_trace[max_it] = self.global_best
        return global_best_trace
    # end def run_nsteps

    def visualize(self,ax,nx=100,cur_pos=True,ind_best=True,glob_best=True):
        import matplotlib.pyplot as plt

        # plot landscape as background
        x = np.linspace(self.xmin,self.xmax,nx)
        grid = np.apply_along_axis(self.landscape,1
            ,[np.array([myx,myy]) for myx in x for myy in x] )
        grid = grid.reshape(nx,nx)
        cs = ax.contour(x,x,grid.T,alpha=0.5)

        # plot population
        if cur_pos:
            ax.scatter(self.pop.T[0],self.pop.T[1],label="current positions")

        if ind_best:
            ax.scatter(self.individual_best_pos.T[0],self.individual_best_pos.T[1]
                ,c="g",alpha=0.7,label="individual best")
        
        if glob_best:
            ax.scatter(self.global_best_pos[0],self.global_best_pos[1],color="r"
		,label="global best")

	#ax.legend(scatterpoints = 1,fontsize=10,loc="best")
        return cs
    # end def visualize

# end class
