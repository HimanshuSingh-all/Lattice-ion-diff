import glob, os, sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from lat2d import newparser

dire = sys.argv[1]  
dataset = '/home/himanshu/Proj/src/Datasets'

data = f'{dataset}/{dire}'

slopes = []

for dirs in sorted(glob.glob(f'{data}/Data-*')):

    with open(f'{dirs}/parameters.txt') as params:

        for line in params:

            keyvalue = line.split(':')
            
            if keyvalue[0] == 'epsilon':
                epsilon = float(keyvalue[1])
            
            if keyvalue[0] == 'WRITE-PERIODICITY':
                WP = float(keyvalue[1])
            
            if keyvalue[0] == 'NSTEPS':
                NSTEPS = int(keyvalue[1])
            
            if keyvalue[0] == 'J':
                J = float(keyvalue[1].rstrip())

            if keyvalue[0] == 'Assignment':
                Assignment = keyvalue[1].rstrip()
            
            if keyvalue[0] == 'Sites Per Vacancy ':
                sitespvac = int(keyvalue[1].rstrip())
 

    # t = np.arange(WP,NSTEPS//2,WP)
    files =glob.glob(f'{dirs}/*-NSTEPS{NSTEPS}.txt')
    diffs = [] # we will fill vacancy, coresponding diffusivity
    for fil in files:
        """ Get the vacancy, diffusivity
        """
        MSD = newparser.time_msd(fil.split('/')[-1], dirs)
        with open(fil) as f:
            print(fil)
            cov = f.readline()
            cov = int( cov.split(':')[-1] )
        diffs.append( [100-cov, stats.linregress( MSD[:,0] , MSD[:,1] ).slope/4.0 ]  )

    diffs = np.array(sorted(diffs,key=lambda x:x[0]))
    with open(f'{dirs}/Diffs-eps{epsilon}','w+') as savefile:
        np.savetxt(savefile, diffs)

    plt.plot(diffs[: ,0] , diffs[:,1], marker ='x',label='E = {0}$k_bT$, J={1}$k_bT$'.format(epsilon,J))
    plt.xticks(diffs[: ,0])
    plt.grid()
    try:
        plt.title(f'Way of Penalty Assignment: {Assignment}, Sites Per vacancy: {sitespvac}')
    except:
        plt.title(f'Diffusivity vs MC step ')
        
    plt.legend()
    plt.ylabel(r'Diffusivity $\to$')
    plt.xlabel(r'Vacancy(%) $\to$')
    plt.savefig(f'{dirs}/Diffs-eps{epsilon}.png', dpi = 300, bbox_inches = 'tight')
    plt.show(block=False)
    plt.pause(0.5)
    plt.close()
