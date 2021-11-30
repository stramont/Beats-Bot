from pymusicxml import Note, Measure, Score, Part
from random import choice, randint

import numpy as np

 # key: A, B, C, D, E, F, G, A'
pitch_bank = ['000', '001', '010', '011', '100', '101', '101', '111'] # length is 8
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

accent_bank = ["","#","b"]

beat_length = ['00', '01', '10', '11'] # eight note, quarter note, half note, whole note

MEASURES = 16

beatLeft = 4.0

ruleDict = {}


def createPiece(genome):
    global ruleDict
    ruleDict = parseGenome(genome) # Creates the rule dictionary
    #left side pred notes, right side resulting notes

    # generate new piece
    measures = []
    previousNote = None

    queryHits = queryCount = 0.0 # Variables used to calculate the percentage of rule hits
    
    for i in range(MEASURES):
        m = Measure(time_signature=(4, 4) if i == 0 else None)
        beatsLeft = 4

        if (i == 0): # generates first note
            newNote, newLength = genRandomNote() # Generates completely random note
            #newNote = "{:d}{:d}{:d}{:d}{:d}".format(genome[0], genome[1], genome[2], genome[3], genome[4])
            #newLength = getBeatOfNote(newNote)
            previousNote = newNote  # saves random note to select next rule
            beatsLeft -= newLength  # updates beats left

            #print(pitch_dict[newNote[:3]] + ", " + getBeatRule(newNote))

            m.append(createNote(newNote))   # appends note to measure
            
        while (beatsLeft > 0):
            nextNote, newLength, hit = getNextNote(previousNote) # Get next note, given by ruleset or random choice

            queryHits = queryHits + 1 if hit else queryHits # Adds one to the number of rule hits if a rule existed for the previous note
            queryCount += 1 # Adds one to the count of total notes hit

            previousNote = nextNote # We do not care if the given note fits, we will use it to determine the next rule either way
            
            if(newLength > beatsLeft): #cuts off notes that exceed remaining beats
                nextNote, newLength = fitNote(nextNote, beatsLeft)

            beatsLeft -= newLength  # updates beats left
            
            #print(pitch_dict[nextNote[:3]] + ", " + getBeatRule(nextNote))

            m.append(createNote(nextNote))
        measures.append(m)

    queryHitPct = queryHits / queryCount

    return measures, queryHitPct


# Parses out map of potential instructions
def parseGenome(g) :
    dict = {}
    for i in range(0, g.size, 10):
        
        key = "{:d}{:d}{:d}{:d}{:d}".format(g[i], g[i+1], g[i+2], g[i+3], g[i+4]) # Creates key from given index on array
        value = "{:d}{:d}{:d}{:d}{:d}".format(g[i+5], g[i+6], g[i+7], g[i+8], g[i+9]) # Creates value from given index on array

        if key in dict:
            dict[key] = np.append(dict[key], [value])
        else:
            dict[key] = [value]

   # for rule in dict.keys():
     #   printRule(rule, dict)

    return dict

    
# Function that returns a random pitch value
def getRandomPitch():
    return pitch_bank[choice(pitch_bank)]


# returning note string (5 bit), and beat (int), plus False as it does not generate a rule from the rule book
def genRandomNote():
    rA = np.random.randint(2,size=5) # creates random 5 length array
    randNote = "{:d}{:d}{:d}{:d}{:d}".format(rA[0], rA[1], rA[2], rA[3], rA[4]) # reformats array into string

    return randNote, getBeatOfNote(randNote), False


# Takes in string of 5 bits, and creates a note from it
def createNote(noteStr):
   # print(getBeatOfNote(noteStr))
    return Note(getPitchOfNote(noteStr), getBeatOfNote(noteStr))


# Gets the 5 bit string of the next note based on the previous note, plus a Boolean value if it uses a rule from the chrome
def getNextNote(prevNote) :
    if prevNote in ruleDict:
        nextNote = choice(ruleDict[prevNote])
        nextNoteLength = getBeatOfNote(nextNote)
        return nextNote, nextNoteLength, True
    else:
        return genRandomNote()


# returns pitch string from note
def getPitchOfNote(note):
    pitch = note[:3]
    return pitch_dict[pitch]


# returns beat int from note
def getBeatOfNote(note):
    beat = note[3:]
    if beat == '00' or beat == '01':
        return 1
    elif beat == '10':
        return 2
    else:
        return 4


# Takes note and beats left, and gives it a new note that fits within the measure
# Returns new fitted note and length of that note
def fitNote(note, beatsLeft):
    newLength = None
    lengths = ["00", "01", "10", "11"]
    
    if beatsLeft == 4:
        newLength = choice(lengths)
    elif beatsLeft >= 2:
        newLength = choice(lengths[:2])
    else:
        newLength = choice(lengths[:1])

    nextNote = note[:3] + newLength
    
    return nextNote, getBeatOfNote(nextNote)


# Prints out the rules associated with the given note
def printRule(note, ruleDict):

    output = "Previous note of " + pitch_dict[note[:3]] + ", " + getBeatRule(note) + " can be: "

    for rule in ruleDict[note]:
        output += pitch_dict[rule[:3]] + ", " + getBeatRule(rule) + " "
    
    print(output)


# Gets the beat associated with the given note, in plain text
def getBeatRule(note):
    noteVal = note[3:]

    if noteVal == "00" or noteVal == "01":
        return "quarter note"
    elif noteVal == "10":
        return "half note"
    else:
        return "whole note"


# parseGenome(g) -> g is a 320 bit array
# returns a dict: 
#   keys 5 bits indicating pitch and beat
#   values 5 bits indicating pitch and beat

# generate a random note: 000 10
# 000 10 sent to dict -> 001 01 -> B4, 4
    # check if measure has space for 4
    # Save prevNote at 001 01 no matter if it fits, generate next note off of it
# createNote(B4, 1)

