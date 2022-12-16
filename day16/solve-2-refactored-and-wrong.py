#
# Advent of Code 2022
# Bryan Clair
#
# Day 16
#
import sys
sys.path.append("..")
import aocutils
from itertools import product

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

import re
parser = re.compile(r"Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.*)$")

nbrs = {}
flow = {}
open_valves = set()
# visited = set()

OUTDEPTH = 13

def pressure(location, timeleft):
    """returns optimal pressure and the path to do it"""
    
    if timeleft == 0:
        return (0,[])

    if timeleft > OUTDEPTH:
        indent = ' '*(30-timeleft)
        print(indent + 'Time:', timeleft, 'Me:',location[0],'El:',location[1])

    # build list of possible moves
    moves = [None,None]
    for who in range(2):
        moves[who] = list(nbrs[location[who]])
        if location[who] not in open_valves and flow[location[who]] > 0:
            moves[who].append('open')
                
    if timeleft > OUTDEPTH:
        print(indent+'Moves:',moves)

#    addvis = [True,True]
#    for who in [0,1]:
#        if location[who] in visited:
#            addvis[who] = False
#        else:
#            visited.add(location[who])

    best = 0
    bestpath = []

    for move in product(moves[0],moves[1]):
        if location[0] == location[1]:
            # don't try (a,b) and (b,a) pairs (small optimization)
            if move[0] > move[1]:
                continue

        if move[0] == move[1] and move[0] != 'open':
            # don't move to the same place
            continue
        
        # don't move somewhere we've already been
#        if move[0] in visited or move[1] in visited:
#            continue
        
        if timeleft > OUTDEPTH:
            print(indent + 'Me: ' + location[0] + ' --> ' + move[0])
            print(indent + 'El: ' + location[1] + ' --> ' + move[1])

        addon = 0
        new_loc = list(move)

        for who in [0,1]:
            if move[who] == 'open':
                open_valves.add(location[who])
                addon += flow[location[who]]*(timeleft - 1)
                new_loc[who] = location[who]
        
        v,path = pressure(new_loc, timeleft - 1)
        v += addon

        for who in [0,1]:
            if move[who] == 'open':
                open_valves.remove(location[who])

        if v > best:
            best = v
            bestpath = [move] + path

#    for who in [0,1]:
#        if addvis[who]:
#            visited.remove(location[who])

    if timeleft > OUTDEPTH:
        print(indent + 'found',best,bestpath)

    return (best,bestpath)

for line in inputlines:
    vname, flows, nbrstr = parser.match(line).groups()
    # print(vname, flows, nbrstr)
    nbrs[vname] = [x.strip() for x in nbrstr.split(',')]
    flow[vname] = int(flows)

print(pressure(('AA','AA'),26))
