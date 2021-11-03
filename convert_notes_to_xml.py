from pymusicxml import *



def convert_to_xml(measures, instrument="Piano",
                   score_title="Algo-Generated Music", file_title="AlgoMusic"):
    """ Creates a .musicxml file from a matrix of pitches and beats (ie notes).

        TODO: add in rests, chords?
              A way to handle notes less than quarter notes, as we need a BeamedGroup for that. """
    
    score = Score(title=score_title, composer="Beats-Bot")
    part = Part(instrument)
    score.append(part)


    #Add the measures to the "part"/instrument created earlier
    part.extend(measures)
    score.export_to_file(file_title + ".musicxml") #Export the file
  

