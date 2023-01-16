import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Tahoma']
"""
The data in rejection ratio file is stored from higher to lower coverage in sorted order.
"""
def returnparams(data:int)->dict:
    params = dict() 
    with open(f'Data-{data}/parameters.txt') as f:
        for lin in f:
            line=lin.split(':')
            params[line[0]] = line[1]
    return params


def plotrejection(data:int, reject:dict,**numvac):
    """
    Plots the rejection ration vs vacancies of a given simulation run.
    # Keyword arguments:
        data: Name of the directory in which a run data is stored
        reject: dictionary of type of rejection ratio values
    """
    number = len(reject['Coverage'])
    if 'numbers' in numvac:
        number = numvac['numbers']

    vac = [100-c for c in reject['Coverage']]
    for key,ratio in reject.items():
        if key=='Coverage': continue
        if key=='EnRejection-Ratio': 
            pass
        print(key)
        plt.scatter(vac[:number], ratio[:number], alpha=0.5, label=key)
    plt.xlabel(r'Vacancy%$\to$')
    plt.ylabel(r'Rejection Ratio$\to$')
    plt.title(r'Rejection Ratio for $\frac{E}{k_BT} =$'+'{0} '.format(returnparams(data)['epsilon']))

def plotset(data:int, reject:dict,**numvac):
    """
    Plots the rejection ration vs vacancies of a given simulation run.
    # Keyword arguments:
        data: Name of the directory in which a run data is stored
        reject: dictionary of type of rejection ratio values
    """
    number = len(reject['Coverage'])
    if 'numbers' in numvac:
        number = numvac['numbers']
    i = None
    if 'i' in numvac: # this will fork only till i =0-11
        i = numvac['i']

    vac = [100-c for c in reject['Coverage']]
    for key,ratio in reject.items():
        if key=='Coverage': continue
        if key=='Rejection-Ratio': 
            plt.plot(vac[:number], ratio[:number], alpha=0.5, marker=i, label=r"$\Delta E_{min}/k_BT$:"+" {0}".format(returnparams(data)['epsilon']))
#        if key=='EnRejection-Ratio': 
#            plt.plot(vac[:number], ratio[:number], alpha=0.5, marker='x', label=r"$\Delta E_{min}/k_BT$:"+" {0}".format(returnparams(data)['epsilon']))
    plt.xlabel(r'Vacancy%$\to$')
    plt.ylabel(r'Rejection Ratio$\to$')
    plt.title(r'Rejection Ratio ')
 
def getrr(data:int)->dict:
    reject = dict()
    with open(f'Data-{data}/newrr.txt') as f:
        for lin in f:
            line=lin.split()
            if line[0] not in reject:
                reject[line[0]] =[ int(line[1])]
                reject[line[6]] = [float(line[7])]
                reject[line[-3]] = [float(line[-1])]
            else:
                reject[line[0]].append( int(line[1]))
                reject[line[6]].append(float(line[7]))
                reject[line[-3]].append(float(line[-1]))

    return reject


if __name__=='__main__':
    #data = int(input(" Enter the name of the file: "))

    #print( getrr(data))
    i=0
    for data in range(2, 12, 3 ):
        plotset(data, getrr(data),i=data-2)#,numbers=10)
    plt.legend()
    plt.savefig(f'rejectionrate-3.png',dpi=300,bbox_inches='tight')
    plt.show()
