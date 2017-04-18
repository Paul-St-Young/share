def parse_gms_inp(gms_inp):
    import numpy as np
    with open(gms_inp) as f:
        text = f.read()
    
    # get inputs
    settings = dict()
    key_val = [token.split('=') for token in text.split() if '=' in token]
    for i in range(len(key_val)):
        key,val = key_val[i]
        settings[key] = val
    
    # get bond length
    idx1 = text.index('$DATA')
    idx2 = text.index('$END')
    all_pos = text[idx1:idx2].split('\n')[3:-1]
    pos1,pos2 = np.array([line.split()[-3:] for line in all_pos],dtype=float)
    dist = round(np.linalg.norm(pos1-pos2),2)
    settings.update({'dist':dist})
    
    return settings

def parse_gms_out(gms_out):
    from mmap import mmap
    fp = open(gms_out,'r+')
    mm = mmap(fp.fileno(),0)

    idx = mm.find('RHF REFERENCE ENERGY')
    mm.seek(idx)
    rhf_line = mm.readline()

    idx = mm.find('EXCITED STATE   1  ENERGY')
    mm.seek(idx)
    ex_line = mm.readline()

    E0 = float(rhf_line.split()[-1])
    E1 = float(ex_line.split()[4])

    fp.close()
    return {'E0':E0,'E1':E1}
