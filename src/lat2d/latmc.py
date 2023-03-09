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

    def __init__(self, 
                args = {'N':20, 'coverage':70, 'epsilon':1.5, 'J':1, 
                'equilibriation':10000, 'assignment':{'way':'vacancy'}}):
        """
        TODO: make the dosctring

        Args:
            args (dict, optional): _description_. Defaults to {'N':20, 'coverage':70, 'epsilon':1.5, 'J':1, 'equilibriation':10000, 'assignment':{'way':'vacancy'}}.

        Raises:
            ValueError: _description_
        """
        #THis is bad, but it will work, ideally one would implement typecheck for the values
        if args['coverage']>=1 or args['coverage']<=0:
            print(f"Coverage of {coverage} bot allowed!!")
            raise ValueError(f"Coverage of {coverage} not allowed!!")

        self.N=args['N']
        self.epsilon=args['epsilon']            # Value of the Energy Penalty
        self.J = args['J']                              #interaction term between ions 
        self.cov=args['coverage']
        self.ions=list()        
        self.rejection = 0                      # number of moves rejected
        self.total = 0                          # total moves proposed
        self.equilibriation = args['equilibriation']    # Equiibriation Steps 
        self.enreject = 0                       # check for the energy metropolis rejection
        self.assignmentstyle = args['assignment']
        
        # NOTE: Always define the lattice before the enlattice, 
        # DO NOT change the ordering
        
        self.init_lattice()                                   
        self.enlattice = self.get_energy_2d(self.assignmentstyle)

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
    
    def get_energy_2d( self, assignment ={'way':'vacancy'}):
        """
        Creates and return the energy penalty lattice.\n
        Keyword Arguments:-\n
        assginment (dict): 
        The way in which we define the enegy lattice.
        It is required to contain the key 'way' which defines the way in which we
        assign the energy penalties. 
        Returns:-\n
        enmatrix (ndarray): A numpy ndaaray of same size as the attendence lattice\n 
                            after applying the site the energy according to the prescribed scheme. 
        """
        #TODO: implement 'random assignment 
        if 'way' not in assignment:
            raise KeyError(' "way" should be a key in the argument assigment dictionary')
        
        
        if assignment['way']=='coordination':  
            choices = [-1, 1]
            enmatrix = np.zeros_like(self.lattice)
            for i, row in enumerate(self.lattice):
                for j, elem in enumerate(row):    
                    if elem==0:
                        horizontal = choices[np.random.randint(2)]
                        vertical = choices[np.random.randint(2)]
                        ##  le '*' denote an oxygen occupied site 'o' be an emty oxygen site 
                        
                        ##   *              *
                        ##     (1)     (2)
                        ##   *      o       *
                        ##     (3)     (4)
                        ##   *      *       *          
                        ##       
                        ##   *      *       *          
                        ## Now we can have a yttria in one of the (1),(2),(3),(4) sites
                        ## Could have implemented loop to do this but im feeling too tired to figure out the logic and 
                        ## this is manageble manually
                        pbcx = (i+horizontal)%self.lattice.shape[0]
                        pbcy = (i+vertical)%self.lattice.shape[1]  
                        enmatrix[i, j]+= self.epsilon
                        enmatrix[pbcx, j]+= self.epsilon
                        enmatrix[i, pbcy]+= self.epsilon
                        enmatrix[pbcx, pbcy]+= self.epsilon    
        
        if assignment['way']=='onvacancy':
            enmatrix = ( np.ones( (self.N,self.N) ) - self.lattice )* self.epsilon
        
        if assignment['way'] == 'random':
            if 'sites_per_vacancy' not in assignment:
                raise KeyError(' For the random way of energy penalty assignment'
                               ' another key value pair of "sites_per_vacancy": '
                               'integer should be in assignment dictionary argument.')

            if type(assignment['sites_per_vacancy']) is not int:
                raise TypeError('The container of "sites_per_vacancy"'
                                'should be of type int.') 
            pass

        return enmatrix

    def init_lattice(self):
        """ initialises the energy lattice """
        self.lattice,self.ionpos=self.get_lattice_2d()
        
        for i,posn in enumerate(self.ionpos):
            self.ions.append(ion(i,posn))
        
        print(f"{self.N}X{self.N} lattice with coverage {self.cov} initialised ({self.cov*self.N*self.N} ions")
        return 
    
    
    
    def mappostolat(self,s,ion_no:int)->tuple:
        """
        Returns 2-tuple of indices for the mapped position of ion onto the lattice if that step is taken\n
        Args:\n
        s(2-D numpy vector): the random next step (coordination number 4) # if None is passed it means no step is taken\n
        Returns:\n
        ion_no (int): index of the ion lattice ion
        """
        if s is None:
            s=np.array((0,0))
        nextstep=np.array(self.ions[ion_no].pos)+s
    
        return tuple(nextstep%self.N)


    def energy_change(self, current_pos:tuple, move_proposed:tuple)->float:
        """Calculates the change of the energy of the system for a given move 
            according to our given prescription.\n

            We consider lattice gas model-like hamiltonian to calculate the energy change.
        """
        def central_energy(index:tuple)->float:
            # TODO: Complete this
            E_ion_pairings = None # calculate ion pairings interaction energy
            pass 

        return central_energy(move_proposed) - central_energy(current_pos)

    def oneionstep(self,ion_no)->None:
        """ Move a given ion using the metropolis algorithm\n

        Keyword Arguments:\n
        ion_no: the index of the ion that will be moved\n

        Returns:\n
        Returns Nothing, but it updates the lattice attribute according to the prescribe metropolis algorithm.\n

        Additional:\n
        # s is an array but class.pos is a tuple,\n
        # so we add them by converting pos into ndarray\n
        # and then revert it back to tuple\n
        """
        MOVES=[(1,0),(0,1),(-1,0),(0,-1)]
        s=np.array(MOVES[np.random.choice([0,1,2,3])])                                      
        new_proposed_position=self.mappostolat(s,ion_no)
        delU=self.enlattice[new_proposed_position]-self.enlattice[self.mappostolat(None,ion_no)]
        rnd=np.random.uniform(0,1)
        prob=np.exp(-delU)
        self.total+=1
        self.ions[ion_no].step+=1

        if self.lattice == 1:
            self.rejection += 1
        else:
            delU= self.energy_change(ion_no)
            #self.enlattice[new_proposed_position]-self.enlattice[self.mappostolat(None,i)]
            rnd=np.random.uniform(0,1)
            prob=np.exp(-delU)
            
            if delU<0 or rnd<prob: #TODO Check the 2nd condition (the condition after or)
                self.lattice[self.mappostolat(None,ion_no)]=0                                         #vacate teh current position in the lattice   
                self.ions[ion_no].pos=tuple(np.array(self.ions[ion_no].pos)+s)                             #update the ion position
                self.lattice[new_proposed_position]=1                                                          #update the new filled position
            else:
                self.rejection += 1
                
        return None

    def onemcstep(self)->None:
        if len(self.ions)!=0:
            [self.oneionstep(i) for i in range(len(self.ions))]
        else:
            self.init_lattice()
            self.onemcstep()
    
    def energy(self, *args, **kwargs)->float:
        """ Returns the Energy of the lattice \n
        
        """ 
        # Use the numpy matrix element by element multiplication as it is faster
        return np.sum( np.multiply( self.lattice , self.enlattice ) ) #

    def average_energy(self)->float:
        """ Returns the average energy of the Lattice """
        a = self.energy()
        return a/len(self.ions)


        
        


if __name__=='__main__':
    
    checklat = lat_2d(3 , 8/9 , 1 , 1000)
    print(checklat.lattice)
    print(checklat.enlattice)
    """
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

    """