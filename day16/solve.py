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

nbrs = {}
flow = {}
nodes = []
decision_nodes = ['AA']

import re
parser = re.compile(r"Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.*)$")
for line in inputlines:
    vname, flows, nbrstr = parser.match(line).groups()
    print(vname, flows, nbrstr)
    nodes.append(vname)
    nbrs[vname] = [x.strip() for x in nbrstr.split(',')]
    flow[vname] = int(flows)
    if flow[vname] > 0:
        decision_nodes.append(vname)

# state of valves is stored as an integer, with bits for each valve
valve_mask = {}
b = 1
for v in decision_nodes[1:]:
    valve_mask[v] = b
    b = b << 1

class Store():
    def __init__(self):
        # array indexed by time of
        # hash table indexed by positions of
        #   (where (a,b) and (b,a) point to the same structure)
        # hash table indexed by valve state
        self.table = []
        self.size = 0
        for time in range(START_TIME+1):
            ptable = {}
            for p0,p1 in product(nodes, nodes):
                if p0 < p1:
                    continue
                vtable = {}
                ptable[(p0,p1)] = vtable
                ptable[(p1,p0)] = vtable
            self.table.append(ptable)
                
    def __getitem__(self,state):
        time,pos,valves = state
        return self.table[time][pos][valves]

    def __setitem__(self,state,pressure):
        self.size += 1
        if self.size % 1000000 == 0:
            print('States:',self.size)
            
        time,pos,valves = state
        
        try:
            self.table[time][pos][valves] = pressure
        except (KeyError, IndexError) as m:
            print('error',time,pos,valves)
            raise(m)

    def display(self,time):
        for pos in self.table[time]:
            if self.table[time][pos]:
                print('--',pos)
                print(self.table[time][pos])


def moves(time, pos, valves):
    # determine possible successor states and the gains by moving there
    move_list = [None,None]
    for who in range(2):
        move_list[who] = list(nbrs[pos[who]])
        if flow[pos[who]] > 0 and not (valve_mask[pos[who]] & valves):
            if who or pos[who] != pos[who-1]:
                move_list[who].append('open')

    return product(move_list[0],move_list[1])

def pressure(time, pos, valves):
    """
    Return the amount of pressure you can relieve starting in this state
    until time runs out. Valves count for pressure only at the moment they
    are opened.
    """
    if time == 0:
        return 0

    if time > OUTDEPTH:
        indent = ' '*(START_TIME-time)
        print(indent + 'Time:', time, 'At:',pos)
    
    try:
        best = pressure_table[time,pos,valves]
        if time > OUTDEPTH:
            print(indent + 'found:',best)
        return best
    except KeyError:
        pass

    # recursively determine the values of the successor states
    # choose the maximum gain + value move.
    best = 0

    for move in moves(time,pos,valves):
        addon = 0
        new_loc = list(move)
        new_valves = valves
        
        for who in [0,1]:
            if move[who] == 'open':
                assert(not (new_valves & valve_mask[pos[who]]))
                addon += flow[pos[who]]*(time-1)
                new_valves = new_valves | valve_mask[pos[who]]
                new_loc[who] = pos[who]
        
        v = addon + pressure(time-1, tuple(new_loc), new_valves)

        if v > best:
            best = v

    if time > OUTDEPTH:
        print(indent + 'calcd:',best)

    pressure_table[time, pos, valves] = best

    return best


START_TIME = 26
OUTDEPTH = 21

pressure_table = Store()

best = pressure(time=START_TIME, pos=('AA','AA'), valves=0))

print('part 2:',best)

# Visits just under 190,000,000 states
# Ran in under 15 minutes
