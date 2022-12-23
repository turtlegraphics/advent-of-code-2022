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

def build_all(stuff, what = 3):
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

def build_limited(stuff):
    """Return a list of buildable vectors, given cost and stuff.
    Has upper limits on how many to consider as well as lower limits
    ensuring you use high-value items.
    However, this is BUGGED and will say it can build nothing when there's
    enough obsidian but not enough ore.
    This requires a global build_limits variable, maybe like so:
    """
    try:
        build_limited.limits
    except AttributeError:
        build_limited.limits = [3*max(cost[0]),
                                2*cost[1,2],
                                cost[2,3],
                                1000]
        print('build limits set to',build_limited.limits)
        
    result = []
    for b in itertools.product(range(5),range(5),range(3),range(3)):
        left = stuff - (cost @ b)
        if np.any(left < 0):
            continue
        if np.any(left >= build_limited.limits):
            # ensure you use materials
            continue
        result.append(b)
    return result

def build_greedy(stuff):
    result = []

    b = np.array([0,0,0,1])
    # build geode cracker if you can
    if all((stuff - cost @ b) >= 0):
        return [b]

    result = []
    # consider building an obsidian robot
    obs = np.array([0,0,1,0])
    if all((stuff - cost @ obs) >= 0):
        result.append(obs)

    # actually, always build obsidian if you can
    if result:
        return result
    
    # consider building a clay robot
    clay = np.array([0,1,0,0])
    if all((stuff - cost @ clay) >= 0):
        result.append(clay)
    
    # consider building an ore robot
    ore = np.array([1,0,0,0])
    if all((stuff - cost @ ore) >= 0):
        result.append(ore)

    # possibly build nothing
    # but don't build nothing if you have a lot of ore
    if stuff[0] < 8:
        result.append(np.zeros(4))
        
    return result

def debug(time, msg):
    """Debug message based on -d argument"""
    if (time > time0 - args.debug):
        tstr = '%2d:' % (time0 - time)
        indent = ' '*(time0-time)
        print(tstr + indent + msg)

def geodes(time, robots, stuff):
    """Find optimum geode production for given cost matrix, robots, stuff"""
    debug(time, 'stuff: '+str(stuff)+' robots: '+str(robots))
    
    if time == 0:
        return stuff[3]
    
    state = (time,tuple(robots),tuple(stuff))
    if state in seen:
        return seen[state]

    best = 0
    best_b = None

    possible = BUILD_FUNCTION(stuff)
    debug(time, ' buildable: '+str(possible))
    
    for b in possible:
        debug(time,' try building '+str(b))
        g = geodes(time-1, robots + b, stuff - (cost @ b) + robots)
        if g > best:
            best = g
            best_b = b

    debug(time, ' best was build  '+str(best_b) + ' to get ' + str(best))

    seen[state] = best
    if len(seen) % 10000 == 0:
        print('!seen:',len(seen))

    global best_geodes
    if best > best_geodes:
        print('!new best: '+str(best))
        best_geodes = best
        
    return best

def test():
    global cost
    cost = blueprints[1]
    stuff0 = np.array([1,0,7,0])  # this is a problem - it gives up instead of waiting
    print(stuff0)
    print(build_limited(stuff0))
    quit()

def blueprint_optimize(b):
    print()
    print('=============')
    print('BLUEPRINT',b)
    print('=============')

    global cost
    global best_geodes
    global seen
    
    best_geodes = 0
    seen = {}
    robot0 = np.array([1,0,0,0])
    stuff0 = np.zeros(4)
    cost = blueprints[b]
    
    result = geodes(time0, robot0, stuff0)
    
    print('finished with',b)
    print('id',b,'cracked',result,'geodes')
    return result

def do_all_blueprints():
    numgeodes = {}

    for b in blueprints:
        numgeodes[b] = blueprint_optimize(b)

    print('='*30)
    print('results')

    quality = 0
    for b in numgeodes:
        print('id',b,'cracked',numgeodes[b],'geodes')
        quality += b*numgeodes[b]

    return quality

blueprints = parse()
time0 = 24
BUILD_FUNCTION = build_greedy

# part 1:
print('part 1:',do_all_blueprints())

# part 2:
time0 = 32
b1 = blueprint_optimize(1)
b2 = blueprint_optimize(2)
b3 = blueprint_optimize(3)
print('part 2:',b1*b2*b3)
