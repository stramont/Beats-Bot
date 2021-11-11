#Genetic Algorithm
#Dr. Reggia's SGA.py algorithm with very minor changes
#Changes include:
#   adding fitness proportion selection
#   adding elitism
#   modifying tournament to allow any given tourney size, not just 2
#   No 2D ant maze simulation

import numpy as np

class algo:
    
    def __init__(self, stringLength, popSize, nGens, pm, pc):
        #Initialize variables
        fid=open("results.txt", "w")
        self.fid = fid
        self.stringLength = stringLength
        self.nGens = nGens
        self.pm = pm
        self.pc = pc
        if np.mod(popSize,2)==0:           # popSize must be even
                self.popSize = popSize
        else:
                self.popSize = popSize+1
        self.pop = np.random.rand(self.popSize,self.stringLength)
        self.pop = np.where(self.pop<0.5,1,0)  # create initial pop
        fitness = self.fitFcn(self.pop)    # fitness values for initial population
        self.bestfit = fitness.max()       # fitness of (first) most fit chromosome
        self.bestloc = np.where(fitness == self.bestfit)[0][0]  # most fit chromosome locn
        self.bestchrome = self.pop[self.bestloc,:]              # most fit chromosome
        self.bestfitarray = np.zeros(self.nGens + 1)  # array of max fitness vals each generation
        self.bestfitarray[0] = self.bestfit           #  (+ 1 for init pop plus nGens)
        self.meanfitarray = np.zeros(self.nGens + 1)  # array of mean fitness vals each generation
        self.meanfitarray[0] = fitness.mean()
        fid.write("popSize: {}  nGens: {}  pm: {}  pc: {}\n".format(popSize,nGens,pm,pc))
        fid.write("initial population, fitnesses: (up to 1st 100 chromosomes)\n")
        for c in range(min(100,popSize)):   # for each of first 100 chromosomes 
           fid.write("  {}  {}\n".format(self.pop[c,:],fitness[c]))
        fid.write("Best initially:\n  {} at locn {}, fitness = {}\n".format(self.bestchrome,self.bestloc,self.bestfit))
        
    def fitFcn(self, pop):
        #compute fitness of population
        #as a numpy array of the fitness of each chromosome
        pop_fitness = []

        for chrome in pop:
            pop_fitness.append(self.fitness_of_chrome(chrome))

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

    def tournament(self, pop, tourney_size=2):
        #Conduct a tournament to select offspring of population

        cand_list1 = []
        cand_list2 = []
        cand_fit1 = []
        cand_fit2 = []
        popsize = len(pop)

        #Choose the index of the tournament candidates
        #as many as were specified
        curr_cands = 0
        while curr_cands < tourney_size:
            cand_index = np.random.randint(popsize)
            
            if cand_index in cand_list1:
                continue
            else:
                cand_list1.append(cand_index)
                curr_cands += 1
        
        #Compare fitnesses of all the candidates and pick the most fit
        for ci in cand_list1:
            cand_fit1.append(self.fitness_of_chrome(pop[ci]))

        cl_array = np.array(cand_list1)
        par1_index = cl_array.argmax() #Get the indices of the maximum fitness
        
        #After choosing the first parent, choose the second
        curr_cands = 0
        while curr_cands < tourney_size:
            cand_index = np.random.randint(popsize)

            if cand_index in cand_list2:
                continue
            else:
                cand_list2.append(cand_index)
                curr_cands += 1

        #Compare the fitness of all the candidates and pick the most fit
        for ci in cand_list2:
            cand_fit2.append(self.fitness_of_chrome(pop[ci]))

        cl_array = np.array(cand_list2)
        par2_index = cl_array.argmax()
        

        #Return the parent indices or the parent chromosomes themselves?
        return par1_index, par2_index

    def fitpselect(self, pop):
        #Find the best of the best of the population
        pop_prob = []
        pop_fit = []
        pop_indices = []

        #Get the fitness for every chromosome
        #NOTE: for this and the probability list pop_prob, the index
        #of the chromosome in pop corresponds to the index in these
        #two lists.
        for i, chrome in enumerate(pop):
            pop_fit.append(self.fitness_of_chrome(chrome))
            pop_indices.append(i)

        fit_array = np.array(pop_fit) #Make sure it's a numpy array
        fit_sum = fit_array.sum() #Get the sum of the fitness values

        #Calculate the probability to  be chosen for each chromosome
        for fitness in fit_array:
            pop_prob.append(fitness / fit_sum)

        #Randomly choose a chromosome based on their given probabilities
        best_index = np.random.choice(pop_indices, 1, pop_prob)
        
        #Return the randomly chosen best fit chromosome
        return best_index

    def elitism(self, pop, num_of_top):
        #Get the top chromosome (indexes) equal to 'num_of_top'
        fit_list = []
        index_list = []
        for chrome in pop:
            fit_list.append(self.fitness_of_chrome(chrome))

        fit_list = np.array(fit_list)

        #Use np.argsort to get the the indices each fitness value would be in
        #when sorted. This is useful because these correspond to the
        #chromosomes the fitnesses came from, so we can 
        sort_indices = np.argsort(fit_list)
        
        for i in range(num_of_top):
            #Get the index of the maximum value.
            #Given the maximum value will be the index for the fitness to be sorted
            #at the very end, this will also be the index of the chromosome with the
            #best fitness
            sort_indices = list(sort_indices) #Must convert to a list to delete from it
            index = sort_indices.pop() #Get the last index
            index_list.append(index)
            sort_indices = np.array(sort_indices) #Back to numpy array to use argmax()

        return index_list

    def run_algo(self,elite_size=2,tournament=True,tourney_size=2): #run the algorithm
        fid = self.fid #output file
        
        for gen in range(self.nGens):
            # initialize new population
            newPop = np.zeros((self.popSize,self.stringLength),dtype = 'int64')
            # create new population newPop via selection and crossovers with prob pc
            for pair in range (0,self.popSize-elite_size,2):
                #tournament or fitpselect
                if tournament:
                    # p1, p2 integers indexes for the chromosomes in self.pop
                    p1, p2 = self.tournament(self.pop,tourney_size) 
                else:
                    p1 = self.fitpselect(self.pop) 
                    p2 = self.fitpselect(self.pop)
                child1 = np.copy(self.pop[p1,:])       # child1 for newPop
                child2 = np.copy(self.pop[p2,:])       # child2 for newPop
                if np.random.rand() < self.pc:                 # with prob self.pc 
                    child1, child2 = self.crossover(child1,child2)  #   do crossover
                newPop[pair,:] = child1                # add offspring to newPop
                newPop[pair + 1,:] = child2

            # mutations to population with probability pm
            newPop = self.mutate(newPop)

            #Elitism: Select the top fitness chromosomes for the next gen
            top_chrome = self.elitism(self.pop, elite_size)
            pop_index = self.popSize-elite_size
            for index in top_chrome:
                newPop[pop_index,:] = self.pop[index]
                pop_index+=1

            self.pop = newPop
            fitness = self.fitFcn(self.pop)    # fitness values for population
            self.bestfit = fitness.max()       # fitness of (first) most fit chromosome
            self.bestloc = np.where(fitness == self.bestfit)[0][0]  # most fit chromosome locn
            self.bestchrome = self.pop[self.bestloc,:]              # most fit chromosome
            if (np.mod(gen,10)==0):            # print epoch, max fitness
                 print("generation: ",gen+1,"max fitness: ",self.bestfit) 
        fid.write("\nfinal population, fitnesses: (up to 1st 100 chromosomes)\n")
        fitness = self.fitFcn(self.pop) #compute final pop fitness
        self.bestfit = fitness.max() #fitness of first most fit chromosome
        self.bestloc = np.where(fitness == self.bestfit)[0][0] #most fit chromosome locn
        self.bestchrome = self.pop[self.bestloc,:] #most fit chromosome
        for c in range(min(100, self.popSize)): #for each of first 100 chromosomes
           fid.write("  {}  {}\n".format(self.pop[c,:],fitness[c])) 
        fid.write("Best:\n  {} at locn {}, fitness: {}\n\n".format(self.bestchrome,self.bestloc,self.bestfit))
        fid.close()
