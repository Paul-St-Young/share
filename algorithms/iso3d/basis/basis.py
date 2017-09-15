#!/usr/bin/env python
import numpy as np

def bfd_basis():
  import pyscf.gto.basis as bas
  basis={ # truncated BFD double-zeta basis set from autogenv2
  'C':bas.parse('''
C s 
 0.205100     0.397529
 0.409924     0.380369
 0.819297     0.180113
 1.637494     -0.033512
 3.272791     -0.121499
 6.541187     0.015176
 13.073594     -0.000705
C s
 0.127852     1.000000
C p
 0.234064     0.302667
 0.468003     0.289868
 0.935757     0.210979
 1.871016     0.112024
 3.741035     0.054425
 7.480076     0.021931
C d
 0.561160     1.000000
  '''),
  }
  return basis
# end def bfd_basis

if __name__ == '__main__':

  from pyscf.pbc import gto
  from pyscf.pbc.dft import gen_grid,numint
  import matplotlib.pyplot as plt
  from mpl_toolkits.mplot3d import Axes3D # enable 3D projection 
  from qharv.inspect import volumetric

  mygs  = 4 # grid density
  alat  = 4.0
  orbs_to_show = set( (('2s',''),('2p','x'),('3d','xy'),('3d','z^2')) )
  assert len(orbs_to_show) == 4 # !!!! hard-code 4 plots

  gs    = np.array([mygs]*3)
  basis = bfd_basis()

  cell = gto.M(a=alat*np.eye(3),atom='C 2.0 2.0 2.0',verbose=3
    ,gs=gs,pseudo={'C':'bfd'},basis=basis)

  coords = gen_grid.gen_uniform_grids(cell)
  aoR    = numint.eval_ao(cell,coords)

  grid_shape = 2*gs+1
  
  fig = plt.figure()
  iplot = 0
  bas_labels = cell.ao_labels(fmt=False)
  for ibas in range( len(bas_labels) ):
    
    iatom,alabel,b_l,b_m = bas_labels[ibas]
    if (b_l,b_m) not in orbs_to_show:
      continue
    iplot += 1

    ax  = fig.add_subplot(2,2,iplot,projection='3d')
    ax.set_title('%s %s %s' % (alabel,b_l,b_m))
    meshm = volumetric.isosurf(ax,aoR[:,ibas].reshape(grid_shape),level_frac=0.28)
    meshm.set_facecolor('#3498db')
    meshm.set_edgecolor('#34495e')
    meshp = volumetric.isosurf(ax,aoR[:,ibas].reshape(grid_shape),level_frac=0.72)
    meshp.set_facecolor('#fb9a99')
    meshp.set_edgecolor('#e11a1c')

  # end for
  fig.savefig('cbas.png',dpi=320)
  plt.show()

# end __main__
