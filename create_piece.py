from pymusicxml import Note, Measure, Score, Part
from random import choice, randint


"""
getNote(beatsLeft, getPitch())

beatsLeft -= returnedLength
"""




pitch_bank = ["a", "b", "c", "d", "e", "f", "g"] # length is 7
accent_bank = ["","#","b"]

beat_length = [1.0, 2.0, 4.0] # eight note, quarter note, half note, whole note

MEASURES = 16

beatLeft = 4.0

def createPiece():

    score = Score(title="Algorithmically Generated RANDOM MusicXML", composer="HTMLvis")
    part = Part("Piano")
    score.append(part)  

    measures = []   # Measures for the piece, to be appended to piece
    
    for i in range(MEASURES):
        m = Measure(time_signature=(4, 4) if i == 0 else None)
        beatsLeft = 4
        while (beatsLeft > 0):
            new_beat = getBeat(beatsLeft)
            beatsLeft -= new_beat
            pitch = getPitch()
            
            m.append(Note(pitch, new_beat))
        measures.append(m)

    part.extend(measures)

    score.export_to_file("AlgorithmicExample.musicxml")


# Function that returns appropriate beat length
def getBeat(beatsLeft) :
    if (beatsLeft >= 4):
        beat_random_value = beat_length[randint(0,2)]
    elif (beatsLeft >= 2):
        beat_random_value = beat_length[randint(0,1)]
    else:
        beat_random_value = beat_length[0]

    return beat_random_value

    
# Function that returns pitch value
def getPitch():
    return choice(pitch_bank) + "4"




createPiece()