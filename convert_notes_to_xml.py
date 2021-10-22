from pymusicxml import *



def convert_to_xml(pitch_matrix, beat_matrix, instrument="Piano", time_sig=(4,4),
                   score_title="Algo-Generated Music", file_title="AlgoMusic"):
    """ Creates a .musicxml file from a matrix of pitches and beats (ie notes).

        TODO: add in rests, chords?
              A way to handle notes less than quarter notes, as we need a BeamedGroup for that. """
    
    score = Score(title=score_title, composer="Beats-Bot")
    part = Part(instrument)
    score.append(part)

    measures = []
    num_measures = len(pitch_matrix) #The number of measures correspond to the number of rows in the pitch matrix

    for i in range(num_measures):
        m = Measure(time_signature=time_sig if i == 0 else None)
        
        #We assume that the proper amount of beats for each measure has been calculated already when creating
        #the note and beat matrix. Therefore, we will not worry about counting the beats when adding notes to the measure
        for j, pitch in enumerate(pitch_matrix[i]):
            m.append(Note(pitch, beat_matrix[i][j])) #Add the note to the measure

        measures.append(m)

    #Add the measures to the "part"/instrument created earlier
    part.extend(measures)
    score.export_to_file(file_title + ".musicxml") #Export the file
  


#------#
# TEST #
#------#

nm = (("a5", "b5", "c5", "d5"),
      ("a5", "b5", "c5", "d5"))
bm = ((1,1,1,1),
      (1,1,1,1))

convert_to_xml(nm, bm)
