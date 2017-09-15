#!/usr/bin/env python
import numpy as np

def generate_timing_data(nx_list,nrepeat=3):
  from skimage import measure
  from datetime import datetime
  
  ymean = []
  yerr  = []
  nrepeat = 3
  for nx in nx_list:
    x0  = 0
    sig = 1.0
    myx = np.linspace(-1,1,nx)
    xyz = np.meshgrid(myx,myx,myx)
    vol = np.sum( np.exp([-(r-x0)**2./sig**2. for r in xyz]), axis=0)

    times = []
    for irep in range(nrepeat+1):
    
      t1 = datetime.now()
      lmin,lmax = vol.min(),vol.max()
      level = lmin + 0.5*(lmax-lmin)
      verts, faces, normals, values = measure.marching_cubes_lewiner(vol, level)
      t2 = datetime.now()
      dt = (t2-t1).microseconds

      if irep > 0: # do not count first run, which may include initialization
        times.append(dt)
      # end if
    # end for
    ymean.append( np.mean(times) )
    yerr.append( np.std(times,ddof=1)/np.sqrt(len(times)) )
  # end for nx

  return ymean,yerr
# end def 

if __name__ == '__main__':
  import os
  import pandas as pd

  dat_json = 'march_times.json'
  if not os.path.isfile(dat_json):
    nlist = np.arange(3,128,8)
    ymean,yerr = generate_timing_data(nlist)
    df = pd.DataFrame({'nx':nlist,'ymean':ymean,'yerr':yerr})
    df.to_json(dat_json)
  else:
    df = pd.read_json(dat_json)
  

  sec = 1000. # ms
  import matplotlib.pyplot as plt
  fig,ax = plt.subplots(1,1)
  ax.set_xlabel('number of grid points',fontsize=16)
  ax.set_ylabel('time (s)',fontsize=16)
  ax.errorbar(df['nx']**3,df['ymean']/sec,yerr=df['yerr'].values[0]/sec,fmt='o')
  fig.tight_layout()
  fig.savefig('cpu_time.png',dpi=320)
  plt.show()

# end __main__
