from lat2d import latmc
write=0
epsilon = 2*2223/1300
equilibriation = 10000
N=20
NSTEPS=50000
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
            fhand.write(f"Coverage:{cov}\n")           
            for i,step in enumerate(range(NSTEPS)):
                mylat.onemcstep()
                if i%WT==0 and i>equilibriation:
                    for io in mylat.ions:
                        fhand.write(f"{io.pos[0]} ")

                    fhand.write("\n ")

                    for io in mylat.ions:
                        fhand.write(f"{io.pos[1]} ")

                    fhand.write("\n")

            with open('newrr.txt','a+') as fhand:  
                fhand.write(f"Coverage:  {cov} : [ Rejection : {mylat.rejection} Total : {mylat.total} Rejection-Ratio : {mylat.rejection/mylat.total} EnRejection : {mylat.enreject} Enrejection-Ratio : {mylat.enreject/mylat.total} ]"+"\n")            

if __name__ == "__main__":
    coverage = [99 ,98, 97, 96, 95, 94, 93,  92, 91, 90, 88, 85, 82, 80, 78, 75, 72, 70, 68, 65, 62, 60, 58, 55, 52, 50]
    import os
    import glob
    nruns = len(glob.glob("Data-*"))
    os.mkdir(f"Data-{nruns}")
    os.chdir(f"Data-{nruns}")
    run_simulations(coverage)
    with open('parameters.txt','w+') as f:
        f.write(f"epsilon:{epsilon} \n")
        f.write(f"WRITE-PERIODICITY:{WT} \n")
        f.write(f"NSTEPS:{NSTEPS} \n")
        f.write(f"EQL:{equilibriation} \n")
        f.write(f"N:{N}")


"""
 fhand.write(f"Created:{day} \n")
 fhand.write(f"Coverage:{cov} \n")
 fhand.write(f"N:{N} \n")
 fhand.write(f"NUM-IONS:{NIONS} \n")
 fhand.write(f"NSTEPS:{NSTEPS} \n")
 fhand.write(f"WRITE-PERIODICITY:{WT} \n")
 """
