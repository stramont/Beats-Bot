from create_piece import createPiece
from pymusicxml import Note, Measure, Score, Part

#Rule conditionals:  If you create a rule, create a new conditional for it
#at the top of this file, and then enclose your rule in the conditional 
#in the function
ALL_QUARTERS = True


def fitness(c): # c = chromosome
    f = 50
    measures = createPiece(c)

    # Raises fitness there are more quarter notes in the first measure
    if ALL_QUARTERS:
        for n in measures[0].leaves():
            if n.written_length == 1.0:
                f += 1


    return f