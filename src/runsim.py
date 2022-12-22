from lat2d import latmc
write=0
epsilon = 2223/1300
equilibriation = 5000
N=20
NSTEPS=15000
WT=100

def run_simulations(coverages:list)->None:
    """ Runs the simulations with the given parameters 
    --Keyword Arguments:
    # coverage(list) : list of coverages 
    """
    for cov in coverages:
        fname=f"{cov}-NSTEPS{NSTEPS}.txt"
        with open(fname,'w+') as fhand: 

            mylat=latmc.lat_2d(N,cov/100,epsilon,equilibriation)
            mylat.init_lattice()
            mylat.init_energylattice()
            NIONS=len(mylat.ions)
           
            for i,step in enumerate(range(NSTEPS)):
                mylat.onemcstep()
                if i%WT==0:
                    for io in mylat.ions:
                        fhand.write(f"{io.pos[0]} ")

                    fhand.write("\n ")

                    for io in mylat.ions:
                        fhand.write(f"{io.pos[1]} ")

                    fhand.write("\n")

if __name__ == "__main__":
    run_simulations([30])
    print(" tactitcs ")
"""
 fhand.write(f"Created:{day} \n")
 fhand.write(f"Coverage:{cov} \n")
 fhand.write(f"N:{N} \n")
 fhand.write(f"NUM-IONS:{NIONS} \n")
 fhand.write(f"NSTEPS:{NSTEPS} \n")
 fhand.write(f"WRITE-PERIODICITY:{WT} \n")
 """
