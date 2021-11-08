#Genetic Algorithm
#Dr. Reggia's SGA.py algorithm with very minor changes

import numpy as np

class algo:
    
    def __init__(self, stringLength, popSize, nGens, pm, pc):
        #Initialize variables
        fid=open("results.txt", "w")
        self.fid = fid
        self.stringLength = stringLength
        self.nGens = nGens
        self.pm = pm
        
    def fitFcn(self, pop):
        #compute fitness of population    
        return 1
        
    def fitness_of_chrome(self, chrome):
        #Compute the fitness of a single chromosome
        return 1

    
    def crossover(self, child1, child2): #Single point crossover between two children/chromosomes
        location = np.random.randint(0, self.stringLength - 1) #pick crossover point
        child1_tmp = np.copy(child1)
        #Do the crossover
        child1[location+1:self.stringLength] = child2[location+1:self.stringLength]
        child2[location+1:self.stringLength] = child1_tmp[location+1:self.stringLength]
        return child1, child2

    #Mutate some chromosomes in population
    def mutate(self, pop):
        #Assign a probability to every chromosome in the pop
        whereMutate = np.random.rand(np.shape(pop)[0],np.shape(pop)[1])
        #if the probability is less than pm, save its location
        whereMutate = np.where(whereMutate < self.pm)

        #For each element in pop that satisfies the above condition,
        #mutate it (1 - chromosome)
        pop[whereMutate] = 1 - pop[whereMutate]
        return pop #returns population with mutations

    def tournament(self, pop, fitness, popsize):
        #Conduct a tournament to select offspring of population
        return 1

    def elitism(self):
        #Find the best of the best of the population
        return 1

    def run_algo(self): #run the algorithm
        fid = self.fid #output file
        for gen in range(self.nGens):
            print("loop")
        fid.write("\nfinal population, fitnesses: (up to 1st 100 chromosomes)\n")
        fitness = self.fitFcn(self.pop) #compute final pop fitness
        self.bestfit = fitness.max() #fitness of first most fit chromosome
        self.bestloc = np.where(fitness == self.bestfit)[0][0] #most fit chromosome locn
        self.bestchrome = self.pop[self.bestloc,:] #most fit chromosome
        for c in range(min(100, self.popSize)): #for each of first 100 chromosomes
           fid.write("  {}  {}\n".format(self.pop[c,:],fitness[c])) 
        fid.write("Best:\n  {} at locn {}, fitness: {}\n\n".format(self.bestchrome,self.bestloc,self.bestfit))
        fid.close()
