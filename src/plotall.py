import glob
import numpy as np
from plotfns import plotMCsteps as MC 
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


def plot_one(plotwhat, fil:str, traj:tuple, path:str,cov,  **kwargs):
    """
    Keyword Arguments:

    """
    data = np.loadtxt(fil)
    if kwargs is None or 'marker' not in kwargs:
        marker = None                               
    else:
        marker = kwargs['marker']

    da = np.vstack([data[:,traj[0]], data[:,traj[1]]])
    print(da.T.shape)
    plotwhat(trajectory = da.T,  marker = marker,cov=cov)
    plt.legend()


def plot_onebyone(plotwhat, path:str, traj:tuple, typ ='energy'):    

    files = glob.glob(f'{path}/*{typ}.txt')
    for fil in files:
        cov = fil.split('/')[-1].split('-')[0] 
        print(cov)
        plot_one(plotwhat, fil, traj, path, int(cov), marker = 'x')
        l = len(glob.glob('*.png')) 
        plt.savefig(f'{path}/{l}-{cov}.png', dpi = 300)
        plt.show(block=False)
        plt.pause(2)
        plt.close()
        
def plot_all(plotwhat, path:str, traj:tuple, typ ='energy', what:str = 'en'):    

    files = glob.glob(f'{path}/*{typ}.txt')
    for fil,marker in zip(files, Line2D.markers):
        cov = fil.split('/')[-1].split('-')[0] 
        print(cov)
        plot_one(plotwhat, fil, traj, path, int(cov), marker = marker)
    l = len(glob.glob('*-all.png')) 
    print(l+1, path)
    plt.savefig(f'{path}/{l+1}-{what}-all.png', dpi = 300)
    plt.show(block = False)
    plt.pause(2)
    plt.close()


if __name__ =='__main__':
    
    se = 6
    fpaths= glob.glob(f"Datasets/Set-{se}/Data-*")
    print(fpaths)
    for pat in fpaths:
        plot_onebyone(MC.plot_energy_vs_steps, pat, (0,1))

    for pat in fpaths:
        plot_onebyone(MC.plot_rejection_vs_steps, pat, (0,2))
    for pat in fpaths:
        plot_all(MC.plot_energy_vs_steps, pat, (0,1))

    for pat in fpaths:
        plot_all(MC.plot_rejection_vs_steps, pat, (0,2), what = 'rr')
