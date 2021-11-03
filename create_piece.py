from pymusicxml import Note, Measure, Score, Part
from random import choice, randint

import numpy as np

 # key: A, B, C, D, E, F, G, A'
pitch_bank = ['000', '001', '010', '011', '100', '101', '101', '111'] # length is 8
pitch_dict = {
    '000': 'A4', 
    '001': 'B4',
    '010': 'C4', 
    '011': 'D4',
    '100': 'E4',
    '101': 'F4',
    '101': 'G4',
    '111': 'A5'
}
accent_bank = ["","#","b"]

beat_length = ['00', '01', '10', '11'] # eight note, quarter note, half note, whole note

MEASURES = 16

beatLeft = 4.0


def createPiece(genome):
    ruleDict = parseGenome(genome) # Creates the rule dictionary
    #left side pred notes, right side resulting notes

    # generate new piece
    measures = []
    previousNote = None
    
    for i in range(MEASURES):
        m = Measure(time_signature=(4, 4) if i == 0 else None)
        beatsLeft = 4

        if (i is 0): # generates first note
            newNote, newLength = genRandomNote(beatsLeft) # Generates completely random note
            previousNote = newNote  # saves random note to select next rule
            beatsLeft -= newLength  # updates beats left
            m.append(createNote(newNote))   # appends note to measure
            
        while (beatsLeft > 0):
            nextNote, newLength = getNextNote(previousNote, ruleDict) # Get next note, given by ruleset or random choice

            previousNote = nextNote # We do not care if the given note fits, we will use it to determine the next rule either way
            
            if(newLength > beatsLeft): #cuts off notes that exceed remaining beats
                nextNote, newLength = fitNote(nextNote, beatsLeft)

            beatsLeft -= newLength  # updates beats left
            
            m.append(createNote(nextNote))

    return measures  


# Parses out map of potential instructions
def parseGenome(g) :
    ruleDict = {}

    for i in range(0, g.length, 10):
        
        key = "{:d}{:d}{:d}{:d}{:d}".format(g[i], g[i+1], g[i+2], g[i+3], g[i+4]) # Creates key from given index on array
        value = "{:d}{:d}{:d}{:d}{:d}".format(g[i+5], g[i+6], g[i+7], g[i+8], g[i+9]) # Creates value from given index on array

        if key in ruleDict:
            ruleDict[key] = np.append(ruleDict[key], [value])
        else:
            ruleDict[key] = [value]

    return ruleDict

    
# Function that returns a random pitch value
def getRandomPitch():
    return pitch_bank[choice(pitch_bank)]


# returning note string (5 bit), and beat (int)
def genRandomNote():
    rA = np.random.randint(2,size=5) # creates random 5 length array
    randNote = "{:d}{:d}{:d}{:d}{:d}".format(rA[0], rA[1], rA[2], rA[3], rA[4]) # reformats array into string

    return randNote, getBeatOfNote(randNote)


# Takes in string of 5 bits, and creates a note from it
def createNote(noteStr):
    return Note(getPitchOfNote(noteStr), getBeatOfNote(noteStr))


# Gets the 5 bit string of the next note based on the previous note
def getNextNote(prevNote, genome) :
    if prevNote in genome:
        nextNote = choice(genome[prevNote])
        nextNoteLength = getBeatOfNote(nextNote)
        return nextNote, nextNoteLength
    else:
        return genRandomNote()


# returns pitch string from note
def getPitchOfNote(note):
    pitch = note[:3]
    return pitch_dict[pitch]


# returns beat int from note
def getBeatOfNote(note):
    beat = note[3:]
    if beat is '00' or '01':
        return 1
    elif beat is '10':
        return 2
    else:
        return 4


# Takes note and beats left, and gives it a new note that fits within the measure
# Returns new fitted note and length of that note
def fitNote(note, beatsLeft):
    newLength = None
    lengths = ["00", "01", "10", "11"]
    
    if beatsLeft is 4:
        newLength = choice(lengths)
    elif beatsLeft is >= 2:
        newLength = choice(lengths[:2])
    else:
        newLength = choice(lengths[:1])

    nextNote = note[:3] + newLength
    
    return nextNote, newLength


createPiece()



# parseGenome(g) -> g is a 320 bit array
# returns a dict: 
#   keys 5 bits indicating pitch and beat
#   values 5 bits indicating pitch and beat

# generate a random note: 000 10
# 000 10 sent to dict -> 001 01 -> B4, 4
    # check if measure has space for 4
    # Save prevNote at 001 01 no matter if it fits, generate next note off of it
# createNote(B4, 1)

