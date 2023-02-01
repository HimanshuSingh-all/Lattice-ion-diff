import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import glob



def givepaths(elem):
    if elem <6:
        print(f"Dataset {elem} doesn't support variance since it is before Set-7") 
        print("ignoring it ...")
        return _
    path = f"Datasets/Set-{elem}"
    for dat in glob.glob(f"{path}/*"):
        if dat.split('.')[-1] == 'png':
            continue
        yield (dat,glob.glob(f"{dat}/*-energy.txt"))

def calc_variance(vector):
    """
    Vector: 1-D numpy array.
    """
    return np.var(vector)


def var_calcs(dir_file:tuple): 
    dire,paths = dir_file
    ret_data = np.zeros((len(paths),2))
    for i,fname in enumerate(paths):
        cov = int(fname.split('/')[-1].split('-')[0])
        edata = np.loadtxt(fname)
        ret_data[i,0],ret_data[i,1] = cov, calc_variance(edata[:,1])
   
    return ret_data




if __name__ == "__main__":

    files = 7
    a=givepaths(files)
    path = f"Datasets/Set-{files}"
    datas = list()
    for dir_file in a:
        dire = dir_file[0]
        with open(f"{dire}/parameters.txt",'r') as fhand:
            eps = fhand.read().split(':')[1].split('\n')[0]
            
            plotit =  var_calcs(dir_file)
            datas.append([int(eps), plotit])
            plt.plot(plotit[:,0], plotit[:,1], alpha = 0.5, marker= 'x')
            plt.xlabel(r'Coverage$\to$')
            plt.ylabel(r'$\sigma_E^2$')
            plt.savefig(f"{dire}/varE-{eps}.png")
    
    n = len(datas)
    print(datas)
    fig,ax = plt.subplots()
    ax.set_prop_cycle('color',[plt.cm.hot(i) for i in np.linspace(0.1, 0.8, n)])
    markers = Line2D.markers
    del markers[None]
    del markers['.']
    del markers[',']
    for evar, marker in zip(datas, markers) :
        eps, variance = evar
        variance = variance[variance[:, 0].argsort()] ## Sorts the variance on the basis of coverage
        ax.plot(variance[:,0], variance[:,1], marker = marker, label = r"$\frac{\Delta E}{k_bT}$:"+f"{eps}")

    ax.set_title('Variance vs Coverage')
    ax.set_xlabel(r'Coverage$\to$')
    ax.set_ylabel(r'$\sigma_E^2$$\to$')
    ax.legend() 
    fig.savefig(f"{path}/varE.png")

