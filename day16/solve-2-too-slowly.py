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

print('This code solves the test case for part 2, so it probably works.')
print('But it will never solve the actual input.')

nbrs = {}
flow = {}
open_valves = set()

OUTDEPTH = 13

def pressure(location, timeleft, camefrom):
    # returns optimal pressure and the path to do it
    if timeleft == 0:
        return (0,[])

    if timeleft > OUTDEPTH:
        indent = ' '*(30-timeleft)
        print(indent + 'Time:', timeleft, 'Me:',location[0],'El:',location[1])

    best = 0
    bestpath = []

    # build list of possible moves
    moves = [None,None]
    for who in range(2):
        moves[who] = list(nbrs[location[who]])
        try:
            moves[who].remove(camefrom[who])
        except ValueError:
            pass
        if location[who] not in open_valves and flow[location[who]] > 0:
            if location[who] != location[1-who]:
                moves[who].append('open')
            else:
                # both could open, only let me do it
                if who == 0:
                    moves[who].append('open')
                    
    if timeleft > OUTDEPTH:
        print(indent+'Moves:',moves)
        
    if (not moves[0]) or (not moves[1]):
        return(0,[])
    
    for me,el in product(moves[0],moves[1]):
        if location[0] == location[1]:
            # we're in the same place, dont try (a,b) and (b,a) pairs
            if me > el:
                continue

        if timeleft > OUTDEPTH:
            print(indent + 'Me: ' + location[0] + ' --> ' + me)
            print(indent + 'El: ' + location[1] + ' --> ' + el)
        addon = 0
        if me == 'open':
            open_valves.add(location[0])
            addon += flow[location[0]]*(timeleft - 1)
            my_new_loc = location[0]
            my_cf = None
        else:
            my_new_loc = me
            my_cf = location[0]
            
        if el == 'open':
            open_valves.add(location[1])
            addon += flow[location[1]]*(timeleft - 1)
            el_new_loc = location[1]
            el_cf = None
        else:
            el_new_loc = el
            el_cf = location[1]

        v,path = pressure((my_new_loc, el_new_loc), timeleft - 1, (my_cf, el_cf))
        v += addon

        if me == 'open':
            open_valves.remove(location[0])
        if el == 'open':
            open_valves.remove(location[1])

        if v > best:
            best = v
            bestpath = [(me,el)] + path

    if timeleft > OUTDEPTH:
        print(indent + 'found',best,bestpath)

    return (best,bestpath)

for line in inputlines:
    vname, flows, nbrstr = parser.match(line).groups()
    # print(vname, flows, nbrstr)
    nbrs[vname] = [x.strip() for x in nbrstr.split(',')]
    flow[vname] = int(flows)

print(pressure(('AA','AA'),26,(None,None)))
