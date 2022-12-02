#
# Advent of Code 2022
# Bryan Clair
#
# Day 02
#
import sys
import re
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

oppTable = {
    'A' : 0,
    'B' : 1,
    'C' : 2
    }
meTable = {
    'X' : 0,
    'Y' : 1,
    'Z' : 2
    }

def score(opp, me):
    win = 0
    if me == opp+1 or (me == 0 and opp == 2):
        win = 6
    elif me == opp:
        win = 3
    return win + me + 1

tot = 0
for line in inputlines:
    opp, me = line.split()
    opp = oppTable[opp]
    me = meTable[me]
    tot += score(opp,me)

print(tot)

tot = 0
for line in inputlines:
    opp, me = line.split()
    opp = oppTable[opp]
    if me == 'X':
        play = (opp - 1) % 3
    elif me == 'Y':
        play = opp
    else:
        play = (opp + 1) % 3
    tot += score(opp,play)

print(tot)


    
