# Beats-Bot
CMSC421 group project

## How to Run
Run with `python3 main_driver.py`.  Evolutionary algorithm parameters
could be edited inside this file.

After running, 5 files will be produced in the current directory: 4 of them are musicXML files,
and one of them is a fitness plot graph.  (4 files are produced because of the slight variations that occur in creating the song)

To listen to one of these musicXML file songs, use a program such as MuseScore: https://musescore.org/en.


## Current Ruleset mapping
000 - c4
001 - d4
010 - e4
011 - f4
100 - g4
101 - a4
110 - b4
111 - c5

00 - Quarter
01 - Quarter
10 - Half
11 - Whole

## Chromosome Details
Each chromosome will have 32 rules, each rule being 10 bits:
 5 bits for the note, 5 bits for the note that should come after
