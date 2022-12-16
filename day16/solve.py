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

import re
parser = re.compile(r"Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.*)$")
for line in inputlines:
    vname, flows, nbrstr = parser.match(line).groups()
    print(vname, flows, nbrstr)
    nbrs[vname] = [x.strip() for x in nbrstr.split(',')]
    flow[vname] = int(flows)

states = []


# pressure so far, time, open valves, locations
start = (0,0,set(),('AA','AA'))
states.append(start)
