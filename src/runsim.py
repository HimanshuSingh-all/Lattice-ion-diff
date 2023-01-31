from lat2d import latmc
import numpy as np
write=0
equilibriation = 10000
N=20
NSTEPS=100000
WT=100

def run_simulations(coverages:list,epsilon:float)->None:
    """ Runs the simulations with the given parameters 
    --Keyword Arguments:
    # coverage(list) : list of coverages 
    """
    for cov in coverages:
        fname=f"{cov}-NSTEPS{NSTEPS}.txt"
        ename=f"{cov}-NSTEPS{NSTEPS}-energy.txt"
        with open(fname,'w+') as fhand, open(ename,'w+') as ehand:

            mylat=latmc.lat_2d(N,cov/100,epsilon,equilibriation)
            NIONS=len(mylat.ions)
            fhand.write(f"Coverage:{cov}\n")           
            for i in range(NSTEPS):
                mylat.onemcstep()

                if i%WT == 0:
                    ehand.write(f"{i} ")
                    ehand.write(f"{mylat.average_energy()} ")
                    ehand.write(f"{mylat.rejection/mylat.total} \n")

                if i%WT==0 and i>equilibriation:
                    for io in mylat.ions:
                        fhand.write(f"{io.pos[0]} ")

                    fhand.write("\n ")

                    for io in mylat.ions:
                        fhand.write(f"{io.pos[1]} ")

                    fhand.write("\n")

            with open('newrr.txt','a+') as fhand:  
                fhand.write(f"Coverage  {cov}  Rejection {mylat.rejection} Total {mylat.total} Rejection-Ratio {mylat.rejection/mylat.total} EnRejection {mylat.enreject} Enrejection-Ratio : {mylat.enreject/mylat.total} "+"\n")            
            
        with open(f'FinalState-{cov}.txt','w+') as fhand:  
            np.savetxt(fhand,mylat.lattice)

        with open(f'FinalENState-{cov}.txt','a+') as fhand:  
            np.savetxt(fhand,mylat.enlattice)
    

if __name__ == "__main__":
    coverage =[100-4*i for i in range(1,7)]#[99 ,98, 97, 96, 95, 94, 93,  92, 91, 90, 88, 85, 82, 80, 78, 75, 72, 70, 68, 65, 62, 60, 58, 55, 52, 50]
    epsilon =[3,4]# [i for i in range(1,4)]
    import os
    import glob
    
    for eps in epsilon:
        nruns = len(glob.glob("Data-*"))
        os.mkdir(f"Data-{nruns}")
        os.chdir(f"Data-{nruns}")
        run_simulations(coverage,eps)
        with open('parameters.txt','w+') as f:
            f.write(f"epsilon:{eps} \n")
            f.write(f"WRITE-PERIODICITY:{WT} \n")
            f.write(f"NSTEPS:{NSTEPS} \n")
            f.write(f"EQL:{equilibriation} \n")
            f.write(f"N:{N}")
        os.chdir("..")


"""
 fhand.write(f"Created:{day} \n")
 fhand.write(f"Coverage:{cov} \n")
 fhand.write(f"N:{N} \n")
 fhand.write(f"NUM-IONS:{NIONS} \n")
 fhand.write(f"NSTEPS:{NSTEPS} \n")
 fhand.write(f"WRITE-PERIODICITY:{WT} \n")
 """
