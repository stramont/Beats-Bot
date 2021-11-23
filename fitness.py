from create_piece import createPiece
from pymusicxml import Note, Measure, Score, Part

#Rule conditionals:  If you create a rule, create a new conditional for it
#at the top of this file, and then enclose your rule in the conditional 
#in the function

ALL_QUARTERS = True

#Raises fitness if the following pattern is detected:
# Measure starts with half note, continues with 2 quarter notes, and 
#next measure is whole note, all decreasing notes.
HALF_QQ_WHOLE_PATTERN = True



pitch_dict = {
    '000': 'c4', 
    '001': 'd4',
    '010': 'e4', 
    '011': 'f4',
    '100': 'g4',
    '101': 'a4',
    '110': 'b4',
    '111': 'c5'
}

pitch_list = ["C", "D", "E", "F", "G", "A", "B", "C"] #For ordering


def fitness(c): # c = chromosome
    f = 50
    measures = createPiece(c)

    # Raises fitness there are more quarter notes in the first measure
    if ALL_QUARTERS:
        for n in measures[0].leaves():
            if n.written_length == 1.0:
                f += 1

      



    return f