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
        #as a numpy array of the fitness of each chromosome
        pop_fitness = []

        for chrome in pop:
            pop_fitness.append(fitness_of_chrome(chrome))

        return np.array(pop_fitness)
        
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

    def tournament(self, pop, popsize, tourn_size=2):
        #Conduct a tournament to select offspring of population

        cand_list1 = []
        cand_list2 = []
        cand_fit1 = []
        cand_fit2 = []

        #Choose the index of the tournament candidates
        #as many as were specified
        curr_cands = 0
        while curr_cands < tourn_size:
            cand_index = np.random.randint(popsize)
            
            if cand_index in cand_list1:
                continue
            else:
                cand_list1.append(cand_index)
                curr_cands += 1
        
        #Compare fitnesses of all the candidates and pick the most fit
        for ci in cand_list1:
            cand_fit1.append(fitness_of_chrome(pop[ci]))

        cl_array = np.array(cand_list1)
        ind = cl_array.argmax() #Get the indices of the maximum fitness
        par1_index = ind[0]   #Since argmax() returns an array, get the first value

        #After choosing the first parent, choose the second
        curr_cands = 0
        while curr_cands < tourn_size:
            cand_index = np.random.randint(popsize)

            if cand_index in cand_list2:
                continue
            else:
                cand_list2.append(cand_index)
                curr_cands += 1

        #Compare the fitness of all the candidates and pick the most fit
        for ci in cand_list2:
            cand_fit2.append(fitness_of_chrome(pop[ci]))

        cl_array = np.array(cand_list2)
        ind = cl_array.argmax()
        par2_index = ind[0]
        

        #Return the parent indices or the parent chromosomes themselves?
        return par1_index, par2_index

    def elitism(self, pop):
        #Find the best of the best of the population
        pop_prob = []
        pop_fit = []

        #Get the fitness for every chromosome
        #NOTE: for this and the probability list pop_prob, the index
        #of the chromosome in pop corresponds to the index in these
        #two lists.
        for chrome in pop:
            pop_fit.append(fitness_of_chrome(chrome))

        fit_array = np.array(pop_fit) #Make sure it's a numpy array
        fit_sum = fit_array.sum() #Get the sum of the fitness values

        #Calculate the probability to  be chosen for each chromosome
        for fitness in fit_array:
            pop_prob.append(fitness / fit_sum)

        #Randomly choose a chromosome based on their given probabilities
        best_index = np.random.choice(pop, 1, pop_prob)
        
        #Return the randomly chosen best fit chromosome
        return pop[best_index]

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
