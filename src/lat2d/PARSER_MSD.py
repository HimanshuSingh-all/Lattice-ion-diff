#TODO: make is such that it picks up the quilibriation form thew file itseld
#TODO:make it so that the 
#Parser MSD
import collections
from scipy import stats
import matplotlib.pyplot as plt
import glob
import numpy as np

def getrunparams(fname,paramlen):
    params=dict()    
    with open(fname) as fhand:
        for i,line in enumerate(fhand):
            if i>=paramlen:
                break
            params[line.split(':')[0]]=line.split(':')[1]
    return params

def getnparray(fname,params:dict,paramlen):
    ndarray=np.loadtxt(fname,skiprows=paramlen)
    return ndarray


def ensemble_sqavg(ndarray,fname,paramlen):
    msdpers=list()
    params=getrunparams(fname,paramlen)
    s=int(params['NUM-IONS'])
    NS=int(params['NSTEPS'])
    WP=int(params['WRITE-PERIODICITY'])
    #print(narray.shape[0]/s,":::")
    for i in range(int(NS/WP-1)): #int(NS/WP-1) 
        #print(int(NS/WP-1))
        #msdpers.append(np.mean( (ndarray[s*(1+i):(i+2)*s,0]-ndarray[s*i:s*(i+1),0])**2+(ndarray[s*(1+i):(i+2)*s,1]-ndarray[s*i:s*(i+1),1])**2))

        #TODO: check the correctness of axis=0 or axis=1
        msdpers.append(np.mean( np.linalg.norm( (ndarray[s*(1+i):(i+2)*s]-ndarray[0:s])**2,axis=1 )))
    return msdpers

#TODO: need better way writing to the file
def time_msd(traj,fname,paramlen,EQUILIBIRIATION=5000):
    #traj: a numpy iXD
    """ gives the mean square displacement (time origin) """ 
    params=getrunparams(fname,paramlen)
    mea=list()
    s=int(params['NUM-IONS'])
    NS=int(params['NSTEPS'])
    WP=int(params['WRITE-PERIODICITY'])
    
    tau=(NS-EQUILIBIRIATION)//(4*WP)
    print(tau)
    for n in range(1,tau+1):
        disp_sq_comp=(traj[n*s::]-traj[:-n*s:])*(traj[n*s::]-traj[:-n*s:]) #traj[:-n:,1:] means that we slice till (lastelement-n)th element  
        disp=np.sum(disp_sq_comp,axis=1)                                 # add the component x and y   
        MSD=np.mean(disp)                                                # take the cumilative average of time origin MSD for all ions  
        mea.append(MSD)
    print("_______________________")
    print(params['Coverage'],fname)
    return mea
