from create_piece import createPiece
from pymusicxml import Note, Measure, Score, Part

#Rule conditionals:  If you create a rule, create a new conditional for it
#at the top of this file, and then enclose your rule in the conditional 
#in the function

#Raises fitness if there are more quarter notes in the first measure (Seb)
ALL_QUARTERS = True

#Raises fitness if the following pattern is detected: (Seb)
# Measure starts with half note, continues with 2 quarter notes, and 
#next measure is whole note, all decreasing notes.
HALF_QQ_WHOLE_PATTERN = True

#Raises fitness if pieces ends with input key,
#and if note is longer than a quarter note
ENDS_IN_KEY = (True, '000')

#Raises fitness if there are no sudden jumps between three notes (Robert)
#NOTE: doesn't account across measures, still todo
#For example c4-b4-d4
NO_SUDDEN_JUMPS = (True, 5,)

# Raises fitness if measure has half or whole notes in it
# Will incentivize more interesting patterns in the piece
HAS_EXTENDED_NOTE = True

# Will use hit percentage for rules from the given chromasome to add the fitness of a given piece
# Weights can be adjusted, must be converted from float
USES_RULES = True

#Raises fitness if it detects two consectutive repeated notes (Adit)
#However, if there are three consectutive repeated notes, the fitness is lowered
TWO_CONSECUTIVE_NOTES = True

#Raises fitness if it detects a measure of all ascending or all descending notes. (Seb)
ASC_DSC_NOTES = True

#Raises fitness if song ends with a dominant cadence (5,7 or 2 to 1)
AUTHENTIC_CADENCE = True

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

pitch_dict_list = ["c4", "d4", "e4", "f4", "g4", "a4", "b4", "c5"]

pitch_list = ["C", "D", "E", "F", "G", "A", "B", "C"] #For ordering



def fitness(c): # c = chromosome
    f = 50
    measures, rulesPercentage = createPiece(c)

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
        l = measures[-1].leaves()
        # old error: if pitch_dict[ENDS_IN_KEY[1]] == l[-1][:3]:  
        if pitch_dict[ENDS_IN_KEY[1]] == (l[-1].pitch.step + str(l[-1].pitch.octave)).lower():
            f+= 1
        if l[-1].written_length >= 2.0:
            f+= 1


    if NO_SUDDEN_JUMPS[0]:
        max_gap = NO_SUDDEN_JUMPS[1] #How far we'll let the notes jump
        for m in measures:
            notes = m.leaves()
            
            pitch_index=[]
            for note in notes:
                index=pitch_list.index(note.pitch.step)
                if note.pitch.step == 'C' and note.pitch.octave == 5:
                    index=len(pitch_list)-1 #It's C5, which will be
                pitch_index.append(index)
                
            if len(notes) == 3:
                #Three notes: one must be a half note
                gap12 = abs(pitch_index[0]-pitch_index[1])
                gap23 = abs(pitch_index[1]-pitch_index[2])

                if gap12 < max_gap or gap23 < max_gap:
                    f += 1
                
            elif len(notes) == 4:
                #All quarter notes
                gap12 = abs(pitch_index[0]-pitch_index[1])
                gap23 = abs(pitch_index[1]-pitch_index[2])
                gap34 = abs(pitch_index[2]-pitch_index[3])
                
                if (gap12 < max_gap or gap23 < max_gap) and (gap23 < max_gap or gap34 < max_gap):
                    f += 1


    if HAS_EXTENDED_NOTE:
        for m in measures:
            notes = m.leaves()
            
            if len(notes) < 4: # Means that measure has at least a half or whole note
                f += 2


    if USES_RULES:
        f += int(rulesPercentage * 20)
    
    if TWO_CONSECUTIVE_NOTES:
        prev_pitch = None
        prev_prev_pitch = None

        for m in measures:
            notes = m.leaves()
            for note in notes:
                curr_pitch = note.pitch.step
                if prev_prev_pitch != None: # if we are still on the first three notes, we are going to ignore any repeats
                    if prev_pitch == curr_pitch:
                        if prev_prev_pitch == curr_pitch:
                            f -= 2
                        else:
                            f += 1
                prev_prev_pitch = prev_pitch
                prev_pitch = curr_pitch

        
    if ASC_DSC_NOTES:

        for m in measures:
            all_asc = True
            all_desc = True
            notes = m.leaves()
            note_list = []

            # Create note_list                
            for n in notes:
                note_list.append((n.pitch.step + str(n.pitch.octave)).lower())
            
            if len(note_list) > 1:

                for i in range(len(note_list) - 1): #goes up to and not including last note

                    #Check ascending
                    if not (pitch_dict_list.index(note_list[i]) < pitch_dict_list.index(note_list[i+1])):
                        all_asc = False

                    #Check descendign
                    if not (pitch_dict_list.index(note_list[i]) > pitch_dict_list.index(note_list[i+1])):
                        all_desc = False

                if all_desc or all_asc:
                    f += 3




                



    if AUTHENTIC_CADENCE:
        l = measures[-1].leaves()
        length = len(l)
        n2 = l[-1].pitch.step                           # n2 is the last note, n1 is the second to last note
        if length == 1:                                 # if the last measure has only one note, n1 is chosen from the previous measure
            l2 = measures[-2].leaves()
            n1 = l2[-1].pitch.step
        else:
            n1 = l[-2].pitch.step
        if n2 == "C":                                   # points are given for ending on the root note
            f += 2
            if n1 == "D" or n1 == "G" or n1 == "B":
                f += 4                                  # additional points given for having an authentic cadence (moving from V (G, B, D) to I (C))
        else:
            f -= 2
                
            
                    

                  

    return f
