import glob, os
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from lat2d import newparser

def returnparams(dire:str)->dict:
    params = dict() 
    with open(f'{dire}/parameters.txt') as f:
        for lin in f:
            line=lin.split(':')
            params[line[0]] = line[1]
    return params

def plotalldiffs(path:str): 

    for dirs in glob.glob(f"{path}/*"):
        if dirs.split('.')[-1]=='png':
            continue

        msd_traj = list()
        print("what",dirs)
        for files in glob.glob(f"{dirs}/*{matchexpr}.txt"):

            fi = files.split("/")[-1]
            cov = int(fi.split("-")[0])
            msd_traj.append([ cov, newparser.time_msd( files.split('/')[-1], dirs)] )     
            msd_traj.sort(key=lambda x: x[0] )
        
        with open(f"{dirs}/parameters.txt",'r') as fhand:
            eps = fhand.read().split(':')[1].split('\n')[0]

            # Plot Difusivity vs Vacancy
        vac = []
        for elem in msd_traj[::-1]:
            vac.append([ 100-elem[0],stats.linregress(elem[1][:,0], elem[1][:,1]).slope/4])
        vac = np.array(vac)
        fig,ax = plt.subplots()
        ax.plot(vac[:,0], vac[:,1],alpha = 0.7, color='red', marker='o') 
        ax.set_title('Diffusivity vs Vacancy')
        ax.set_xlabel(r'Vacancy$\to$')
        ax.set_ylabel(r'Diffusivity$\to$')
        ax.legend() 
        fig.savefig(f"{dirs}/diff{eps}.png",dpi=400)
        np.savetxt(f"{dirs}/diff{eps}.txt",vac)

def plotone(fullpath:str,steps:int):
    
    msd_traj = list()
    for files in glob.glob(f"{fullpath}/*NSTEPS{steps}.txt"):
        fi = files.split("/")[-1]
        cov = int(fi.split("-")[0])
        msd_traj.append([ cov, newparser.time_msd( files.split('/')[-1], fullpath)] )     
        msd_traj.sort(key=lambda x: x[0] )

    with open(f"{fullpath}/parameters.txt",'r') as fhand:
        eps = fhand.read().split(':')[1].split('\n')[0]

        # Plot Difusivity vs Vacancy
    vac = []

    for elem in msd_traj[::-1]:
        vac.append([ 100-elem[0],stats.linregress(elem[1][:,0], elem[1][:,1]).slope/4])
    vac = np.array(vac)
    
    fig,ax = plt.subplots()
    ax.plot(vac[:,0], vac[:,1],alpha = 0.7, color='red', marker='o') 
    ax.set_title(r'Diffusivity vs Vacancy $E=3k_bT$')
    ax.set_xlabel(r'Vacancy$\to$')
    ax.set_ylabel(r'Diffusivity$\to$')
    ax.legend() 

    fig.savefig(f"{fullpath}/diff{eps}.png",dpi=400)
    np.savetxt(f"{fullpath}/diff{eps}.txt",vac)

if __name__ == '__main__':

    files = 11
    path = f"Datasets/Set-{files}"
    datas = list()
    NSTEPS = int( input("Enter the number of steps for a walk: ") )
    matchexpr = f"NSTEPS{NSTEPS}"              #input('Enter the end match expression: ')
    
    plotall=int(input("Plotall (1 for YES | 0 for NO): "))

    if plotall:
        plotalldiffs(path)
    else:
        data = int(input("Enter the file: "))
        plotone(f"{path}/Data-{data}",100000)
    

