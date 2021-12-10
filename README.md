# Beats-Bot
CMSC421 group project

## How to Run
Run with `python3 main_driver.py`.  Evolutionary algorithm parameters
could be edited inside this file.

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
