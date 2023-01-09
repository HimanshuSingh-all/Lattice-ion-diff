from lat2d import latmc
from numpy import ones
import glob

def test(testdir:str,NSTEPS:int, lat):
    lens = len(glob.glob('{testdir}/Test-*.txt'))+1
    with open(f'{testdir}/Test-{lens}.txt','w+') as fhand:
        NIONS=len(lat.ions)
        for i,step in enumerate(range(NSTEPS)):
            lat.onemcstep()
            if i%100==0 and i>lat.equilibriation:
                for io in lat.ions:
                    fhand.write(f"{io.pos[0]} ")
                fhand.write("\n ")
                for io in lat.ions:
                    fhand.write(f"{io.pos[1]} ")
                fhand.write("\n")

    with open(f'{testdir}/newrr{lens}.txt','a+') as fhand:  
        print( f'Rejection: {lat.rejection/lat.total}, Energy-Rejection: {lat.enreject/lat.total}' )
        fhand.write(f"Rejection {lat.rejection} Total {lat.total} Rejection-Ratio {lat.rejection/lat.total} EnRejection {lat.enreject} Enrejection-Ratio : {lat.enreject/lat.total} "+"\n")

    with open(f'{testdir}/lattice{lens}.txt','a+') as fhand:  
        fhand.write(f'Lattice: \n {lat.lattice} \n En-Lattice: \n {lat.enlattice}')


lat = latmc.lat_2d(20, 0.5, 9,0)
lat.init_lattice()
lat.enlattice = lat.epsilon * ( ones((20,20)) )#- lat.lattice )
print( lat.lattice, lat.enlattice, lat.lattice+lat.enlattice//9) 
NSTEPS = 50000
import os 
testdir = 'Metropolis-Test'
try:
    os.mkdir(testdir)
    test(testdir,NSTEPS,lat)
except FileExistsError:
    test(testdir,NSTEPS,lat)

    
    







