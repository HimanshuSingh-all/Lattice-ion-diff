import matplotlib.pyplot as plt


def plotrejection(data:int, reject:dict):
    vac = [100-c for c in reject['Coverage']]
    for key,ratio in reject.items():
        if key=='Coverage': continue
        plt.scatter(vac, ratio, alpha=0.5, label=key)
    plt.xlabel(r'Vacancy%$\to$')
    plt.ylabel(r'Rejection Ratio$\to$')
    plt.legend()
    plt.show()
 
def getrr(data:int)->dict:
    reject = dict()
    with open(f'Data-{data}/newrr.txt') as f:
        for lin in f:
            line=lin.split(':')
            if line[0] not in reject:
                reject[line[0]] =[ int(line[1])]
                reject[line[4].split()[1]] = [float(line[5].split()[0])]
                reject[line[-2].split()[1]] = [float(line[-1].split()[0])]
            else:
                reject[line[0]].append( int(line[1]))
                reject[line[4].split()[1]].append(float(line[5].split()[0]))
                reject[line[-2].split()[1]].append(float(line[-1].split()[0]))

    return reject


if __name__=='__main__':
    data = int(input(" Enter the name of the file: "))

    print( getrr(data))
    plotrejection(data, getrr(data))
