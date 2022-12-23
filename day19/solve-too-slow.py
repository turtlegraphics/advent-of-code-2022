#
# Advent of Code 2022
# Bryan Clair
#
# Day 19
#
import sys
import re
import numpy as np
import itertools

sys.path.append("..")
from aocutils import *

args = parse_args()

models = {
    'ore':0,
    'clay':1,
    'obsidian':2,
    'geode':3
}


def parse():
    """
    Parse input to produce blueprints, which are coded as cost matrices.
    A cost matrix has, for example:
       cost[models['clay'],models['obsidian']]
    giving the cost in clay to build an obsidian robot.
    """
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
                        v[models[s]] = int(p)
                    costs.append(v)
            blueprints[id] = np.transpose(np.array(costs))
    return blueprints

def buildable(stuff, what = 3):
    """Return a list of buildable vectors, given cost and stuff,
    only building robots of type what or larger."""

    if what < 0:
        return [np.zeros(4)]

    result = []
    b = np.zeros(4)
    leftover = stuff
    while np.all(leftover >= 0):
        for s in buildable(leftover, what - 1):
            result.append(s + b)
        b[what] += 1
        leftover = stuff - (cost @ b)
    return result

def buildable2(stuff):
    result = []
    for b in itertools.product(range(5),range(5),range(3),range(3)):
        left = stuff - (cost @ b)
        if np.any(left < 0):
            continue
        if np.any(left >= build_limits):
            # ensure you use materials
            continue
        result.append(b)
    return result

def geodes(time, robots, stuff):
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

    possible = buildable2(stuff)
    if (time > display_time):
        print(indent+'buildable:',possible)
    for b in possible:
        g = geodes(time-1, robots + b, stuff - (cost @ b) + robots)
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

if False:
    cost = blueprints[1]
    build_limits = [3*max(cost[0]),
                    2*cost[1,2],
                    cost[2,3],
                    1000]
    stuff0 = np.array([1,0,7,0])  # this is a problem - it gives up instead of waiting
    print(stuff0)
    print(buildable2(stuff0))
    quit()

display_time = 6
time0 = 19

numgeodes = {}
for b in blueprints:
    print('working on',b)

    best_geodes = 0
    seen = {}
    robot0 = np.array([1,0,0,0])
    stuff0 = np.zeros(4)
    cost = blueprints[b]
    build_limits = [3*max(cost[0]),
                    2*cost[1,2],
                    cost[2,3],
                    1000]
    print('build limits:',build_limits)
    
    numgeodes[b] = geodes(time0, robot0, stuff0)
    
    print('finished with',b)
    print('id',b,'cracked',numgeodes[b],'geodes')

print('='*30)
print('results')

quality = 0
for b in numgeodes:
    print('id',b,'cracked',numgeodes[b],'geodes')
    quality += b*numgeodes[b]

print('part 1:',quality)
