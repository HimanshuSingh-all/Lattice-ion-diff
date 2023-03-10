from lat2d import latmc
import numpy as np
write=0
equilibriation = 10000
N=20
NSTEPS= 100000
WT=100
J=1
ENASSIGNMENT = {'way':'onvacancy'}

#TODO: UPDATE how the lat_2d object is initailised.

def run_simulations(coverages:list,epsilon:float, ion_interaction:float)->None:
    """ Runs the simulations with the given parameters 
    Keyword Arguments:
        coverage(list) : list of coverages(in%) in range of 0-100, the function 
        will automatically convert it into the range of 0 to 1. 

        epsilon(float) : The value of energy penalty (in terms of kT).

        ion_interaction(float) : the nearest neighbour interaction energy between the ions 
        (in terms of kT).

    """
    for cov in coverages:
        fname=f"{cov}-NSTEPS{NSTEPS}.txt"
        ename=f"{cov}-NSTEPS{NSTEPS}-energy.txt"
        import time
        init = time.time()
        with open(fname,'w+') as fhand, open(ename,'w+') as ehand:
            
            runparams = {
                            'N':N,
                            'coverage': cov/100,
                            'J':J,
                            'epsilon':epsilon,
                            'equilibriation':equilibriation,
                            'assignment': ENASSIGNMENT
                        }
            
            mylat=latmc.lat_2d(runparams)
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
                fhand.write( ( f"Coverage  {cov}  Rejection {mylat.rejection} Total {mylat.total}"
                               f"Rejection-Ratio {mylat.rejection/mylat.total} EnRejection {mylat.enreject}"
                               f" Enrejection-Ratio : {mylat.enreject/mylat.total} \n"
                            ) )            
        with open(f'FinalState-{cov}.txt','w+') as fhand:  
            np.savetxt(fhand,mylat.lattice)

        with open(f'FinalENState-{cov}.txt','a+') as fhand:  
            np.savetxt(fhand,mylat.enlattice)
        final = time.time()
        print(f'time taken for cov:{cov} is {final-init}')
        print("_________")

    

if __name__ == "__main__":
    coverage = [100 - 4*v for v in range(1,9)]
    epsilon =[ 1, 2 ] 
    import os
    import glob

    for eps in epsilon:
        nruns = len(glob.glob("Data-*")) 
        os.mkdir(f"Data-{nruns}")
        os.chdir(f"Data-{nruns}")
        run_simulations(coverage, eps, J)
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
