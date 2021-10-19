# Ant Route-Finder problem, directional agent in antSGA.py

import pylab as pl
import numpy as np
import random

class sga:

  def __init__(self,stringLength,popSize,nGens,pm,pc):
        # stringLength: int, popSize: int, nGens: int, 
        # probability mutation pm: float; probability crossover pc: float
        fid=open("results.txt","w")        # open, initialize output file
        self.fid = fid
        self.stringLength = stringLength
        if np.mod(popSize,2)==0:           # popSize must be even
                self.popSize = popSize
        else:
                self.popSize = popSize+1
        self.pm = pm                       # probability of mutation
        self.pc = pc                       # probability of crossover
        self.nGens = nGens                 # max num generations
        self.pop = np.random.rand(self.popSize,self.stringLength)
        self.pop = np.where(self.pop<0.5,1,0)  # create initial pop
        self.env =  np.array([             # environment: 0 = empty, 1 = barrier
          [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],           
          [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
          [1,0,0,0,0,0,0,0,1,1,1,0,0,1,1,1,0,0,0,1],
          [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,0,1],
          [1,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1],
          [1,0,0,0,1,1,0,0,1,0,0,1,1,1,1,0,0,0,0,1],
          [1,1,1,0,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1],
          [1,0,1,0,0,0,1,1,0,0,0,0,0,1,0,1,1,1,0,1],
          [1,0,0,0,0,0,1,1,1,0,0,0,0,1,0,0,0,0,0,1],
          [1,0,0,0,1,1,1,0,0,0,1,1,1,0,1,0,0,0,0,1],
          [1,0,1,0,1,1,1,0,0,0,0,1,0,0,0,1,0,0,0,1],   
          [1,0,1,0,0,0,0,0,0,1,1,1,0,0,0,0,1,0,0,1],
          [1,0,1,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
          [1,0,0,0,0,0,0,0,1,0,0,0,0,1,1,1,1,0,0,1],
          [1,1,1,1,1,1,1,1,1,0,1,1,0,1,0,0,0,0,0,1],
          [1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,1,1,1],
          [1,0,0,1,1,1,1,0,0,0,0,1,0,1,0,0,0,0,0,1],
          [1,0,0,0,1,1,1,1,0,0,0,1,0,1,1,1,0,0,0,1],
          [1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1],
          [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]])
        self.tMax = 50                     # max time to run agent simulation 
        self.initLocx = 1                  # agent's original location x,y
        self.initLocy = 1
        self.initDir = 'D'                 # agent's original orientation (URDL) 
        self.goalLocx = 18                 # goal's location x,y
        self.goalLocy = 18
        self.numrules = 10                 # number of rules in chromosome
        self.rulesize = 7                  # number of bits in rule
        self.cw  = {'U':'R','R':'D','D':'L','L':'U'}   # rotate orientation cw
        self.ccw = {'U':'L','R':'U','D':'R','L':'D'}   # rotate orientation ccw
        self.legalActs = np.array(['NG','GF','GR','GL'])    # legal agent actions
        if self.numrules * self.rulesize != self.stringLength:
           print("ERROR: ill formed chromosome size in sga")
           return
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
        self.bestcall = self.bestchrome   # best chromosome all generations
        self.bestfall = self.bestfit      # and its fitness

  def fitFcn(self,pop):         # compute pop fitness 
     fitness = np.ones(self.popSize)      # initialize fitness values (1D array)
     for i in range(self.popSize):        # for each individual in the population
       fitness[i] = self.fitInd(pop[i])   #   compute its fitness
     return fitness

  def fitInd(self,chrome):      # compute and return fitness of a single chromosome
     rules = np.reshape(chrome,(self.numrules,self.rulesize))  # numrules rules, each rulesize bits
     fit = self.simulate(rules,self.tMax)  # simulate agent for tMax time steps
     return fit                            # return agent's (chromesome's) fitness

  # The ant simulator that runs a simulation and returns the agent's (ant's) fitness. 
  # It is initially configured to simulate the ant using the rules extracted from the
  # current chromosome. MODIFY THIS FUNCTION TO COMPUTE THE FITNESS OF THE CHROMOSOME. 
  def simulate(self,rules,tMax):  # simulate rules tMax time steps, return fitness 
     x = self.initLocx            # agent's initial x,y coordinates
     y = self.initLocy
     dir = self.initDir           # agent's initial orientation (direction)  
     fitness = 1.0                # agent's fitness (computed at end)
     for t in range(tMax):         # simulate the agent for tMax time steps t
       if((x == self.goalLocx) and (y == self.goalLocy)):   # at each time step, if at goal
         atGoal = True             # True when in goal state, False when not
       else: atGoal = False
       view = self.sees(x,y,dir,self.env)  # visual field, 1D array: L,LF,F,RF,R  
       r = self.rulematch(rules,view)      # find matching rule, or none
       if np.size(r) != 0:               # first of agent's rules that applies
         action = self.decode(r[5:7])    # decode r's 2 bits to 'NG'/'GF'/'GR'/'GL' 
       else:                             # none of agent's rules apply
         action = self.legalActs[random.randint(0,3)]  # random default action 
       x,y,dir = self.userule(action,x,y,dir)   # apply rule to get agent's new state
     return fitness

  def sees(self,x,y,dir,env):     # returns what agent at x,y sees in direction dir 
     adj = np.array([env[x-1,y-1],env[x-1,y],env[x-1,y+1],env[x,y+1], 
                     env[x+1,y+1],env[x+1,y],env[x+1,y-1],env[x,y-1]]) # adjacent cells, cw
     if dir == 'U':                  # if looking UP
       return np.array([adj[7],adj[0],adj[1],adj[2],adj[3]])
     elif dir == 'R':                # else if looking RIGHT   
       return adj[1:6]
     elif dir == 'D':                # else if looking DOWN
       return adj[3:8]
     elif dir == 'L':                # else if looking LEFT
       return np.array([adj[5],adj[6],adj[7],adj[0],adj[1]])
     else:
       print("ERROR IN sees(): unrecognized dir = ",dir,"\n")
       return np.zeros(5)

  def rulematch(self,rules,view):  # if rule's antecs match visual field, return it; else array([])
     for i in range(np.shape(rules)[0]):     # for each rule i
        r = rules[i,:]                       # r is ith rule
        if np.alltrue(r[0:5] == view):       # if all antecs match view
          return r                           # return the matching rule
     return np.array([])                     # no rules match (return empty array)

  def userule(self,act,x,y,dir):   # take action act at locn x,y having orientation dir    
     if act == 'GF':               # if action is Go Forward, return agent's new state
        if   dir == 'U': newx = x-1; newy = y; newdir = dir
        elif dir == 'R': newx = x; newy = y+1; newdir = dir
        elif dir == 'D': newx = x+1; newy = y; newdir = dir
        elif dir == 'L': newx = x; newy = y-1; newdir = dir
        else:
          print("ERROR in userule(): unrecognized dir = ",dir)
          return x,y,dir
     elif act == 'GR':             # if action is Go Right, return agent's new state
        if   dir == 'U': newx = x; newy = y+1; newdir = self.cw[dir]
        elif dir == 'R': newx = x+1; newy = y; newdir = self.cw[dir]
        elif dir == 'D': newx = x; newy = y-1; newdir = self.cw[dir]
        elif dir == 'L': newx = x-1; newy = y; newdir = self.cw[dir]
        else:
          print("ERROR in userule(): unrecognized dir = ",dir)
          return x,y,dir
     elif act == 'GL':             # if action is Go Left, return agent's new state
        if   dir == 'U': newx = x; newy = y-1; newdir = self.ccw[dir]
        elif dir == 'R': newx = x-1; newy = y; newdir = self.ccw[dir]
        elif dir == 'D': newx = x; newy = y+1; newdir = self.ccw[dir]
        elif dir == 'L': newx = x+1; newy = y; newdir = self.ccw[dir]
        else:
          print("ERROR in userule(): unrecognized dir = ",dir)
          return x,y,dir
     elif act == "NG":             # if action is No Go, return agent's old state
          newx = x; newy = y; newdir = dir
     else:
        print("ERROR unrecognized action in userule(): ",act)
        return x,y,dir
     if self.env[newx,newy] == 1:    # if would be in wall at new location 
        return x,y,dir               # return agent's old state unchanged
     return newx,newy,newdir         # return agent's new state

  def decode(self,bits):           # decode two-bit chromosome actions
    if   np.alltrue(bits == np.array([0,0])): return 'GF'  # 00 is Go Forward
    elif np.alltrue(bits == np.array([0,1])): return 'GR'  # 01 is Go Right
    elif np.alltrue(bits == np.array([1,0])): return 'GL'  # 10 is Go Left
    elif np.alltrue(bits == np.array([1,1])): return 'NG'  # 11 is No Go (no change)
    else:
      print("ERROR IN decode(): unrecognized bits = ",bits,"\n")
      return 'GF'

  # conducts tournaments twice to select two offspring
  # YOU CAN MODIFY THIS IF YOU WANT TOURNAMENTS OF A DIFFERENT SIZE
  def tournament(self,pop,fitness,popsize):  # fitness array, pop size
     # select first parent par1
     cand1 = np.random.randint(popsize)      # candidate 1, 1st tourn., int
     cand2 = cand1                           # candidate 2, 1st tourn., int
     while cand2 == cand1:                   # until cand2 differs
        cand2 = np.random.randint(popsize)   #   identify a second candidate
     if fitness[cand1] > fitness[cand2]:     # if cand1 more fit than cand2
        par1 = cand1                         #   then first parent is cand1
     else:                                   #   else first parent is cand2
        par1 = cand2
     # select second parent par2
     cand1 = np.random.randint(popsize)      # candidate 1, 2nd tourn., int
     cand2 = cand1                           # candidate 2, 2nd tourn., int
     while cand2 == cand1:                   # until cand2 differs
        cand2 = np.random.randint(popsize)   #   identify a second candidate
     if fitness[cand1] > fitness[cand2]:     # if cand1 more fit than cand2
        par2 = cand1                         #   then 2nd parent par2 is cand1
     else:                                   #   else 2nd parent par2 is cand2
        par2 = cand2
     return par1,par2

  def xover(self,child1,child2):    # single point crossover
        # cut locn to right of position (hence subtract 1)
        locn = np.random.randint(0,self.stringLength - 1)
        tmp = np.copy(child1)       # save child1 copy, then do crossover
        child1[locn+1:self.stringLength] = child2[locn+1:self.stringLength]
        child2[locn+1:self.stringLength] = tmp[locn+1:self.stringLength]
        return child1,child2

  def mutate(self,pop):            # bitwise point mutations
        whereMutate = np.random.rand(np.shape(pop)[0],np.shape(pop)[1])
        whereMutate = np.where(whereMutate < self.pm)
        pop[whereMutate] = 1 - pop[whereMutate]
        return pop

  def runGA(self):     # run simple genetic algorithme
        fid=self.fid   # output file
        for gen in range(self.nGens): # for each generation gen
           # Compute fitness of the pop
           fitness = self.fitFcn(self.pop)  # measure fitnesses 
           # initialize new population
           newPop = np.zeros((self.popSize,self.stringLength),dtype = 'int64')
           # create new population newPop via selection and crossovers with prob pc
           for pair in range(0,self.popSize,2):  # create popSize/2 pairs of offspring
               # tournament selection of two parent indices
               p1, p2 = self.tournament(self.pop,fitness,self.popSize)  # p1, p2 integers
               child1 = np.copy(self.pop[p1,:])       # child1 for newPop
               child2 = np.copy(self.pop[p2,:])       # child2 for newPop
               if np.random.rand() < self.pc:                 # with prob self.pc 
                  child1, child2 = self.xover(child1,child2)  #   do crossover
               newPop[pair,:] = child1                # add offspring to newPop
               newPop[pair + 1,:] = child2
           # mutations to population with probability pm
           newPop = self.mutate(newPop)
           self.pop = newPop                  # new population becomes current population
           fitness = self.fitFcn(self.pop)    # fitness values for new population
           self.bestfit = fitness.max()       # fitness of (first) most fit chromosome
           self.bestloc = np.where(fitness == self.bestfit)[0][0]  # most fit chromosome locn
           self.bestchrome = self.pop[self.bestloc,:]              # most fit chromosome
           if self.bestfit > self.bestfall:   # if current chromosome best seen so far
             self.bestcall = self.bestchrome  #   record the new best chromosome
             self.bestfall = self.bestfit     #   and its fitness 
           self.bestfitarray[gen + 1] = self.bestfit        # save best fitness for plotting
           self.meanfitarray[gen + 1] = fitness.mean()      # save mean fitness for plotting
           if (np.mod(gen,10)==0):            # print epoch, max fitness
                print("generation: ",gen+1,"max fitness: ", self.bestfit)
        fid.write("\nfinal population, fitnesses: (up to 1st 100 chromosomes)\n")
        fitness = self.fitFcn(self.pop)         # compute final population fitnesses
        self.bestfit = fitness.max()            # fitness of (first) most fit chromosome
        self.bestloc = np.where(fitness == self.bestfit)[0][0]  # most fit chromosome locn
        self.bestchrome = self.pop[self.bestloc,:]              # most fit chromosome
        for c in range(min(100,self.popSize)):  # for each of first 100 chromosomes
           fid.write("  {}  {}\n".format(self.pop[c,:],fitness[c])) 
        fid.write("Best:\n  {} at locn {}, fitness: {}\n\n".format(self.bestchrome,self.bestloc,self.bestfit))
        fid.close()
        pl.ion()      # activate interactive plotting
        pl.xlabel("Generation")
        pl.ylabel("Fitness of Best, Mean Chromosome")
        pl.plot(self.bestfitarray,'kx-',self.meanfitarray,'kx--')
        pl.show()
        pl.pause(0)