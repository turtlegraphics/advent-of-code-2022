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

    models = {
        'ore':0,
        'clay':1,
        'obsidian':2,
        'geode':3
    }

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

def build(stuff, robots):
    """Given stuff, determine a list of things to consdier building.
    - Always build geode cracker if possible (probably correct)
    - Always build obsidian robot if possible (questionably correct)
    - Always build *something* if you have 8 or more stuff (questionably correct)
    """
    
    result = []

    b = np.array([0,0,0,1])
    # build geode cracker if you can
    if all((stuff - cost @ b) >= 0):
        return [b]

    result = []
    # consider building an obsidian robot
    obs = np.array([0,0,1,0])
    if all((stuff - cost @ obs) >= 0):
        # you can afford it, but do you already have enough?
        if robots[2] < maxrobots[2]:
            result.append(obs)

    # actually, always build obsidian if you can
    if result:
       return result
    
    # consider building a clay robot
    clay = np.array([0,1,0,0])
    if all((stuff - cost @ clay) >= 0):
        # you can afford it, but do you already have enough?
        if robots[1] < maxrobots[1]:
            result.append(clay)
    
    # consider building an ore robot
    ore = np.array([1,0,0,0])
    if all((stuff - cost @ ore) >= 0):
        # you can afford it, but do you already have enough?
        if robots[0] < maxrobots[0]:
            result.append(ore)

    # possibly build nothing
    # but don't build nothing if you have a lot of ore
    if result:
        if stuff[0] < 12:
            result.append(np.zeros(4))
        return result
    else:
        return([np.zeros(4)])

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
    
    state = (tuple(robots),tuple(stuff))
    if state in seen:
        seen_time, seen_score = seen[state]
        if time == seen_time:
            return seen_score
        if time < seen_time:
            # this branch is not as good, kill it
            return -1
        # we've seen this state before but never this early
        
    best = 0
    best_b = None

    if time > 1:
        possible = build(stuff, robots)
    else:
        possible = [np.zeros(4)]  # don't bother building in last minute
        
    debug(time, ' buildable: '+str(possible))
    
    for b in possible:
        debug(time,' try building '+str(b))
        g = geodes(time-1, robots + b, stuff - (cost @ b) + robots)
        if g > best:
            best = g
            best_b = b

    debug(time, ' best was build  '+str(best_b) + ' to get ' + str(best))

    seen[state] = (time,best)

    if len(seen) % 10000 == 0:
        print('!seen:',len(seen))

    global best_geodes
    if best > best_geodes:
        print('!new best: '+str(best))
        best_geodes = best
        
    return best

from timeit import default_timer as timer
from datetime import timedelta

def blueprint_optimize(b):
    """Calculate and return the optimum number of geodes for this blueprint."""
    print()
    print('=============')
    print('BLUEPRINT',b)
    print('=============')
    
    global cost         # cost matrix
    global maxrobots    # max robots we need of any type
    global seen         # store of seen states

    global best_geodes  # only used to output progress
    
    start_time = timer()

    best_geodes = 0
    seen = {}
    robot0 = np.array([1,0,0,0])
    stuff0 = np.zeros(4)
    cost = blueprints[b]
    maxrobots = np.amax(cost,axis=1)
    
    result = geodes(time0, robot0, stuff0)

    end_time = timer()
    
    print('finished with blueprint',b)
    print('id',b,'cracked',result,'geodes')
    print('compute time:',timedelta(seconds = round(end_time - start_time)))
    return result

def do_blueprints(targets):
    """Loop through all blueprints,
    calculate the optimal geodes for each,
    return a dictionary of their scores.
    """
    scores = {}
    for b in targets:
        scores[b] = blueprint_optimize(b)

    print('='*30)
    print('RESULTS')
    for b,score in scores.items():
        print('id',b,'cracked',score,'geodes')
        
    return scores

def quality(scores):
    """Calculate the quality for part 1."""
    quality = 0
    for b,score in scores.items():
        quality += b*score
    return quality

def product(scores):
    """Scores is a dictionary, so no good shortcuts."""
    product = 1
    for b,score in scores.items():
        product *= score
    return product

    
blueprints = parse()
part1 = None

# part 1:
time0 = 24

part1 = quality(do_blueprints(blueprints))
print('part 1:',part1)

# part 2:
time0 = 32
part2 = product(do_blueprints([1,2,3]))
print('part 1:',part1)  # print again so it's not lost in output stream
print('part 2:',part2)
