import glob, os
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from lat2d import newparser


data = int( input("Number of the simulation directory: "))
dire = f"Data-{data}"

#coverage = [5 , 8, 10, 12, 15, 18, 20, 22, 25, 28, 30, 32, 35, 38, 40]

files = glob.glob(f"{dire}/*.txt")
D =[]
for fname in files:
    if fname ==f'{dire}/parameters.txt' or fname ==f'{dire}/newrr.txt':
        continue
    fi = fname.split("/")[1]
    cov = int(fi.split("-")[0])
    print(fi, cov)
    D.append([ cov, newparser.time_msd( fi, dire)] )     

D.sort(key=lambda x: x[0] )
print(D[1])
vac = []
for elem in D:
    vac.append([ 100-elem[0],stats.linregress(elem[1][:,0], elem[1][:,1]).slope/4])

vac = np.array(vac)
plt.plot(vac[:,0], vac[:,1])
plt.show()
