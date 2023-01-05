import glob, os
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from lat2d import newparser
num = 24#Default Val should be: 24

def returnparams(data:int,dset:int)->dict:
    params = dict() 
    with open(f'Set-{dset}/Data-{data}/parameters.txt') as f:
        for lin in f:
            line=lin.split(':')
            params[line[0]] = line[1]
    return params
dset = 2# [1,2]#int( input("Number of the simulation set: "))
star = 17
data = [i for i in range(star,20)] #int( input("Number of the simulation directory: "))


#coverage = [5 , 8, 10, 12, 15, 18, 20, 22, 25, 28, 30, 32, 35, 38, 40]
for dat in data:

    dire = f"Set-{dset}/Data-{dat}"
    files = glob.glob(f"{dire}/*.txt")
    D =[]
    for fname in files:
        if fname ==f'{dire}/parameters.txt' or fname ==f'{dire}/newrr.txt':
            continue
        fi = fname.split("/")[-1]
        cov = int(fi.split("-")[0])
        print(fi, cov)
        D.append([ cov, newparser.time_msd( fi, dire)] )     

    D.sort(key=lambda x: x[0] )
    print(D[1])
    vac = []
    plt.xlabel(r'$Vacancy(\%)\to$')
    plt.ylabel('$Diffusivity\to$')
    for elem in D[::-1]:
        vac.append([ 100-elem[0],stats.linregress(elem[1][:,0], elem[1][:,1]).slope/4])

    vac = np.array(vac)
    plt.plot(vac[:num,0], vac[:num,1],alpha = 0.7, marker=dat-15, label= r"$E_{min}/k_BT=$"+"{0}".format(returnparams(dat,2)['epsilon']) )

plt.legend()
diff = input('Enter diff:')
plt.savefig(f'diff{diff}.png', dpi= 300, bbox_inches='tight')
plt.show()
"""
for elem in D[-10:]:
    plt.plot(elem[1][:,0], elem[1][:,1], label=f'Vacancy:{100-elem[0]}%')
plt.legend()
plt.show()
"""




