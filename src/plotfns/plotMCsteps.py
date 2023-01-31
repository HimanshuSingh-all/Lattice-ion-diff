import numpy as np
import matplotlib.pyplot as plt


def plot_energy_vs_steps( trajectory, **kwargs ):
    """
    trajectory ( nX2 ndarray): MCStep vs Energy of lattice
    **kwargs: for plot parameters
    """
    if kwargs is None or 'marker' not in kwargs:
        marker = None
        cov ='' 
    else:
        marker = kwargs['marker']
        cov = kwargs['cov']

    plt.title("Energy vs MCSteps")
    plt.xlabel(r"MC Step $\to$")
    plt.ylabel(r"Energy$(k_bT)$ $\to$")
    plt.plot(trajectory[:,0], trajectory[:,1], marker = marker, label = f"Coverage: {cov}", alpha = 0.5, markersize=5,markevery=5)
    
def plot_rejection_vs_steps( trajectory, **kwargs):
    """
    trajectory ( nX2 ndarray): MCStep vs Energy of lattice
    **kwargs: for plot parameters
    """
    if kwargs is None or 'marker' not in kwargs:
        marker = None
        cov = ''
    else:
        cov = kwargs['cov']
        marker = kwargs['marker']

    plt.title("Rejection-Ratio vs MCSteps")
    plt.xlabel(r"MC Step $\to$")
    plt.ylabel(r"Rejection-Ratio $\to$")
    plt.plot(trajectory[:,0], trajectory[:,1], marker = marker, label = f"Coverage: {cov}", alpha = 0.5, markersize =6, markevery=5)


if __name__=="__main__":
    
    cov = 96
    steps = 100000

    filepath=f"../Data-2/"
    file=f"../Data-2/{cov}-NSTEPS{steps}-energy.txt"
    
    with open(file,"r") as fhand:
        traj = np.loadtxt(fhand)
        
        plot_energy_vs_steps(traj[:,:2],alpha = 0.5, marker = 'o', label = f"Coverage: {cov}")
        plt.savefig(f"{filepath}coverage-{cov}-EvsMCSTEPS.png", dpi = 300)
        plt.show()
        plot_rejection_vs_steps(traj[:,:3:2],alpha = 0.5, marker = 'o', label = f"Coverage: {cov}")
        plt.savefig(f"{filepath}coverage-{cov}-RRvsMCSTEPS.png", dpi = 300)
        plt.show()
