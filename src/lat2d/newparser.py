#TODO: make is such that it picks up the quilibriation form thew file itseld       
#TODO:make it so that the 
#Parser MSD
import collections
from scipy import stats
import matplotlib.pyplot as plt
import glob
import numpy as np

def getrunparams(dire:str)->(dict,int):
    """ Searches for one parameters.txt file on default in the specified folder then returns the run parameters (dictionary) and the length 
    ** Keyword Arguments:
    # dire: name of the directory in which the simulation data from a run is stored
    _______________________________________________________________________________________________________________________________________
    **Returns:
    # ( params:dict , len(params): int ): dictionary of params and number of parameters 
    """
    fname= glob.glob("{dire}/parameters.txt")
    if fname is None:
        raise FileNotFoundError(" The pramaeters file doesn't exist, make sure the paramets file is named 'parameters.txt")
    params = dict()
    with open(f'{dire}/parameters.txt') as fhands: 
        for fhand in fhands:
            line_ = fhand.rstrip()
            words = line_.split(':')
            params[words[0]] = words[1]
    
    return ( params, len( params.keys() ) )

                 

def getnparray(dire:str, fname:str):
    """ returns the data from the run of the simulation as (2*Steps) X ions sized numpy array 
    ** Keyword Arguments:
    # dire  : name of the directory in which the simulation data from a run is stored
    # fname : name of the simulation run file.
    _______________________________________________________________________________________________________________________________________
    """
    ndarray=np.loadtxt(fname)
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


def time_msd(fname,dire,EQUILIBIRIATION=5000,**test):
    #traj: a numpy iXD
    """ gives the mean square displacement (time origin)
    ** Keyword Arguments:
    # fname: name of the simulation run file
    # dire : directory in which the file is
    # EQUILIBIRIATION : thermalisation time step length   
    _______________________________________________________________________________________________________________________________________
    ** Returns:
    # [[ t, MSD(t) ]]
    """
    if 'test' in test or test['test']:
        params,_=getrunparams(dire)                               # get the run parameters
        s=int(params['NUM-IONS'])
        NS=int(params['NSTEPS'])
        WP=int(params['WRITE-PERIODICITY']) 
        tau=(NS-EQUILIBIRIATION)//(2*WP)
        traj = getnparray(fname , dire)
        x = traj[::2]
        y = traj[1::2]
        print(tau)
        print(f"Opened this {fname} file:")
    else:
        traj = np.loadtxt(fname)
        x = traj[::2]
        y = traj[1::2]
        tau = x.shape[0]//2 

    mea=list()
    if x.shape != y.shape:
        raise ValueError(" x and y don't have same dimensions ")

    for n in range(1,tau+1):
        xdiff = x[n:]-x[:-n]
        ydiff = y[n:]-y[:-n]
        singlePartMean = (xdiff**2 + ydiff**2).sum(axis=0)/(x.shape[0]-n)
        ensembleSinglePartMean = singlePartMean.mean() 
        mea.append( [n, ensembleSinglePartMean] )
         
    print("_______________________")
    print(params['Coverage'],fname)
    return mea
