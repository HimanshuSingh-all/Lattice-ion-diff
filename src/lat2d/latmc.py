import numpy as np
from datetime import date
np.random.seed()

class ion:
    def __init__(self,i:int,pos:tuple):
        self.i=i        #assign an index to the ion
        self.pos=pos    #pos (y,x) of the ion in the space (which will be later mapped on the lattice)
        self.init=pos   #init position of ion in space 
        self.step=0     #to calculate the rejection ratio



class lat_2d:

    def __init__(self, N:int, coverage:float, epsilon:float, equilibriation:int):
        
        if coverage>=1 or coverage<=0:
            print(f"Coverage of {coverage} bot allowed!!")
            raise ValueError(f"Coverage of {coverage} not allowed!!")

        self.N=N
        self.epsilon=epsilon                    # Value of the Energy Penalty
        self.cov=coverage
        self.ions=list()        
        self.rejection = 0                      # number of moves rejected
        self.total = 0                          # total moves proposed
        self.equilibriation = equilibriation    # Equiibriation Steps 
        self.enreject = 0                       # check for the energy metropolis rejection
        self.init_lattice()
        self.init_energylattice()

    def get_lattice_2d(self):
        """
        creates and return 2 tuple of lattice occupation/attendence matrix and list of ion objects, is a buffer function
        """
        A=np.array([(i,j) for i in range(self.N) for j in range(self.N)])
        B=np.arange(0,self.N**2)
        ionc=list()                                                             #contains the intial position of all the occupying lattice ions
        choice=np.random.choice(B,int(self.cov*self.N*self.N),replace=False)    #replace = False to make sure that the we dont put the two ions on one site, impossible also, causing the net coverage to be less
        lattice=np.zeros((self.N,self.N))

        for b in choice:
            lattice[ tuple(A[b]) ]=1 
            ionc.append(tuple(A[b]))    

        return (lattice, ionc)

    def get_energy_2d(self,sites:int):
        """
        creates and return the energy penalty lattice
        Keyword Arguments: 
        sites-- the number of energy packets (sites is probably not correct terminology as on site can get multiple energy packets)
        """
        A=np.array([(i,j) for i in range(self.N) for j in range(self.N)])
        B=np.arange(0,self.N**2)
        ionc=list()                                                             #contains the intial position of all the occupying lattice ions
        choice=np.random.choice(B,int(sites))#self.cov*self.N*self.N
        lattice=np.zeros((self.N,self.N))
        for b in choice:
            lattice[ tuple(A[b]) ]+=self.epsilon 
            
        return lattice
    
    def init_lattice(self):
        """ initialises the energy lattice """
        self.lattice,self.ionpos=self.get_lattice_2d()
        for i,posn in enumerate(self.ionpos):
            self.ions.append(ion(i,posn))
        print(f"{self.N}X{self.N} lattice with coverage {self.cov} initialised ({self.cov*self.N*self.N} ions")

    def init_energylattice(self,fac=2):
        """ 
        initialises the energy penalty lattice 
        """
        self.enlattice=self.epsilon * ( np.ones( (self.N,self.N) ) - self.lattice )
        print(f"{self.N}X{self.N} energy lattice with coverage {self.cov} initialised penalties)")
        print(self.enlattice)
        print("_________")

    def mappostolat(self,s,i:int):
        """
        returns 2-tuple of indices for the mapped position of ion onto the lattice if that step is taken
        Args:
        s(2-D numpy vector): the random next step (coordination number 4) # if None is passed it means no step is taken
        Returns:
        i(int): index of the ion lattice ion
        """
        if s is None:
            s=np.array((0,0))
        nextstep=np.array(self.ions[i].pos)+s
        return tuple(nextstep%self.N)
        

    def oneionstep(self,i):
        """ Move a given ion using the metropolis algorithm

        Keyword Arguments:
        i-- the index of the ion

        Additional:
        # s is an array but class.pos is a tuple,
        # so we add them by converting pos into ndarray
        # and then revert it back to tuple
        """
        MOVES=[(1,0),(0,1),(-1,0),(0,-1)]
        s=np.array(MOVES[np.random.choice([0,1,2,3])])                                      
        latposn=self.mappostolat(s,i)
        delU=self.enlattice[latposn]-self.enlattice[self.mappostolat(None,i)]
        rnd=np.random.uniform(0,1)
        prob=np.exp(-delU)
        self.total+=1
        self.ions[i].step+=1

        if self.lattice[latposn]!=1 and prob>=rnd:                                            #if there is no ion in the step chosen
            self.lattice[self.mappostolat(None,i)]=0                                         #vacate teh current position in the lattice   
            self.ions[i].pos=tuple(np.array(self.ions[i].pos)+s)                             #update the ion position
            self.lattice[latposn]=1                                                          #update the new filled position
        elif prob<rnd:
            self.rejection += 1
            self.enreject +=1
        else:
            self.rejection += 1
        return None

    def onemcstep(self):
        if len(self.ions)!=0:
            [self.oneionstep(i) for i in range(len(self.ions))]
        else:
            self.init_lattice()
            self.onemcstep()
    
    def energy(self, *args, **kwargs):
        """ Returns the Energy of the lattice """ 
        return np.sum( np.multiply( self.lattice , self.enlattice ) )

    def average_energy(self):
        """ Returns the average energy of the Lattice """
        a = self.energy()
        return a/len(self.ions)


        
        


if __name__=='__main__':
    write=0
    N=20
    NSTEPS=100000
    WT=100
    today=date.today()

    coverage=[10.0,20.0,30.0,40.0,50.0,60.0,70.0,80.0,90.0]
    for cov in coverage:
        day=today.strftime("%B-%d-%Y")
        fname=f"simdata/Coverage-{cov}-NSTEPS{NSTEPS}-{day}.txt"
        with open(fname,'w+') as fhand: 
            mylat=lat_2d(N,cov/100)
            mylat.init_lattice()
            NIONS=len(mylat.ions)
            fhand.write(f"Created:{day} \n")
            fhand.write(f"Coverage:{cov} \n")
            fhand.write(f"N:{N} \n")
            fhand.write(f"NUM-IONS:{NIONS} \n")
            fhand.write(f"NSTEPS:{NSTEPS} \n")
            fhand.write(f"WRITE-PERIODICITY:{WT} \n")
            for i,step in enumerate(range(NSTEPS)):
                mylat.onemcstep()
                if i%WT==0:
                    for io in mylat.ions:
                        fhand.write(f"{io.pos[0]}  {io.pos[1]} \n")

