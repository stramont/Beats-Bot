import main_algo

#Main driver for the algorithm

#initialize algo object:
gen_algo = main_algo.algo(320, 50, 50, .01, .05)
# stringLength, popSize, nGens, pm, pc

#Run algorithm
gen_algo.run_algo(5)
# Arguments optional: elite_size, tournament, tourney_size
# default arguments: 2, True, 2