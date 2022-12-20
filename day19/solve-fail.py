#
# Advent of Code 2022
# Bryan Clair
#
# Day 19
#
import sys
import re
import numpy as np

sys.path.append("..")
from aocutils import *

args = parse_args()

def parse():
    indexes = {
        'ore':0,
        'clay':1,
        'obsidian':2,
        'geode':3
    }

    bpparse = re.compile(r"Blueprint (\d+)") # or whatever
    costparse = re.compile(r"Each (\w+) robot costs (.*)$") # or whatever
    inputlines = [x.strip() for x in open(args.file).readlines()]

    blueprints = {}
    for line in inputlines:
        if line:
            id,bp = line.split(':')
            id = int(bpparse.match(line).groups()[0])
            costs = []
            for c in bp.split('.'):
                c = c.strip()
                if c:
                    v = [0,0,0,0]
                    who,what = costparse.match(c.strip()).groups()
                    prices = what.split('and')
                    for thing in prices:
                        p,s = thing.split()
                        s = s.strip()
                        v[indexes[s]] = int(p)
                    costs.append(v)
            blueprints[id] = np.transpose(np.array(costs))
                
    return blueprints

def buildable(cost, stuff, what = 3):
    """Return a list of buildable vectors, given cost and stuff,
    only building robots of type what or larger."""

    if what < 0:
        return [np.zeros(4)]

    result = []
    b = np.zeros(4)
    leftover = stuff
    while np.all(leftover >= 0):
        for s in buildable(cost, leftover, what - 1):
            result.append(s + b)
        b[what] += 1
        leftover = stuff - (cost @ b)
    return result

def geodes(cost, time, robots, stuff):
    """Find optimum geode production for given cost matrix, robots, stuff"""
    if time == 0:
        return stuff[3]

    if (time > display_time):
        indent = ' '*(24-time)
        print(indent+'time',time,'stuff',stuff,'robots',robots)
    
    state = (time,tuple(robots),tuple(stuff))
    if state in seen:
        return seen[state]

    best = 0
    best_b = None

    possible = buildable(cost, stuff)
    if (time > display_time):
        print(indent+'buildable:',possible)
    for b in possible:
        g = geodes(cost, time-1, robots + b, stuff - (cost @ b) + robots)
        if g > best:
            best = g
            best_b = b

    if (time > display_time):
        print(indent+':building',best_b,'to get',best)
        
    seen[state] = best
    if len(seen) % 10000 == 0:
        print('!seen:',len(seen))

    global best_geodes
    if best > best_geodes:
        print('!new best:',best)
        best_geodes = best
        
    return best

blueprints = parse()

# print(buildable(blueprints[1],np.array([4,14,7,3])))

display_time = 0
time0 = 10

numgeodes = {}
for b in blueprints:
    best_geodes = 0
    seen = {}
    robot0 = np.array([1,0,0,0])
    stuff0 = np.zeros(4)
    print('working on',b)
    numgeodes[b] = geodes(blueprints[b], time0, robot0, stuff0)
    print('finished with',b)
    print('id',b,'cracked',numgeodes[b],'geodes')

print('='*30)
print('results')

quality = 0
for b in numgeodes:
    print('id',b,'cracked',numgeodes[b],'geodes')
    quality += b*numgeodes[b]

print('part 1:',quality)
