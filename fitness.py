from create_piece import createPiece
from pymusicxml import Note, Measure, Score, Part

#Rule conditionals:  If you create a rule, create a new conditional for it
#at the top of this file, and then enclose your rule in the conditional 
#in the function

#Raises fitness if there are more quarter notes in the first measure
ALL_QUARTERS = True

#Raises fitness if the following pattern is detected:
# Measure starts with half note, continues with 2 quarter notes, and 
#next measure is whole note, all decreasing notes.
HALF_QQ_WHOLE_PATTERN = True

#Raises fitness if pieces ends with input key,
#and if note is longer than a quarter note
ENDS_IN_KEY = True, '000'

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

    if HALF_QQ_WHOLE_PATTERN:
            for i in range(len(measures)):
                if i != len(measures) - 1:
                    l = measures[i].leaves()
                    if l[0].written_length == 2.0:
                        if l[1].written_length == 1.0 and pitch_list.index(l[1].pitch.step) < pitch_list.index(l[0].pitch.step):
                            if l[2].written_length == 1.0 and pitch_list.index(l[2].pitch.step) < pitch_list.index(l[1].pitch.step):
                                if measures[i+1].leaves()[0].written_length == 4.0:
                                    f += 1

    if ENDS_IN_KEY[0]:
        l = measures[measures.len - 1].leaves()
        if pitch_dict[ENDS_IN_KEY[1]] == l[l.len - 1]:
            f+= 1
        if l[l.len - 1].written_length >= 2.0:
            f+= 1



    return f