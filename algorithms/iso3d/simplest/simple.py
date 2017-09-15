#!/usr/bin/env python
import numpy as np

def isosurf(ax,vol,level_frac=0.25):
  """ draw iso surface of volumetric data on matplotlib axis at given level

  Example usage:
    from mpl_toolkits.mplot3d import Axes3D # enable 3D projection
    vol = np.random.randn(10,10,10)
    fig = plt.figure()
    ax  = fig.add_subplot(1,1,1,projection='3d')
    isosurf(ax,vol)
    plt.show()
  
  Args:
    ax (plt.Axes3D): ax = fig.add_subplot(1,1,1,projection="3d")
    vol (np.array): 3D volumetric data having shape (nx,ny,nz) 
    level_frac (float): 0.0->1.0, isosurface value as a fraction between min and max
  Returns:
    Poly3DCollection: mesh
  ffect:
    draw on ax """
  from skimage import measure
  from mpl_toolkits.mplot3d.art3d import Poly3DCollection
  nx,ny,nz = vol.shape
  lmin,lmax = vol.min(),vol.max()

  level = lmin + level_frac*(lmax-lmin)
  if level<lmin or level>lmax:
      raise RuntimeError('level must be >%f and < %f'%(lmin,lmax))
  # end if

  # make marching cubes
  verts, faces, normals, values = measure.marching_cubes_lewiner(
      vol, level)

  for name,dat in zip(['vertices','faces','vert[faces]'],[verts,faces,verts[faces]]):
    print(name)
    print(dat)

  # plot surface
  mesh = Poly3DCollection(verts[faces])
  mesh.set_edgecolor('k')
  ax.add_collection3d(mesh)
  ax.set_xlim(0,nx)
  ax.set_ylim(0,ny)
  ax.set_zlim(0,nz)
  ax.set_xlabel('x')
  ax.set_ylabel('y')
  ax.set_zlabel('z')
  print('isovalue: %f'%level)
  return mesh
# end def isosurf

if __name__ == '__main__':

  import matplotlib.pyplot as plt
  from mpl_toolkits.mplot3d import Axes3D # enable 3D projection 

  nx  = 3
  x0  = 0
  sig = 1.0
  myx = np.linspace(-1,1,nx)
  xyz = np.meshgrid(myx,myx,myx)
  val = np.sum( np.exp([-(r-x0)**2./sig**2. for r in xyz]), axis=0)
  print('3D volumetric data:')
  print(val)
  
  fig  = plt.figure()
  ax   = fig.add_subplot(1,1,1,projection='3d')
  mesh = isosurf(ax,val,level_frac=0.8)
  mesh.set_facecolor('#3498db')
  mesh.set_edgecolor('#34495e')

  fig.tight_layout()
  fig.savefig('gauss%d.png'%nx,dpi=320)
  plt.show()

# end __main__
