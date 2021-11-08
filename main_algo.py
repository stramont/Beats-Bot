#Genetic algorithm, based on Dr. Reggia's SGA.py algorithm

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
        whereMutate = np.random.rand(np.shape(pop)[0],np.shape(pop)[1])
        whereMutate = np.where(whereMutate < self.pm)
        print(pop)
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
        fid.close()
