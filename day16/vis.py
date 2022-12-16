#
# Advent of Code 2022
# Bryan Clair
#
# Day 16
#


"""
Generate graph output in a format that can be put into Mathematica
so I can visualize these two graphs
"""

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

for line in inputlines:
    vname, flows, nbrstr = parser.match(line).groups()
    # print(vname, flows, nbrstr)
    nbrs[vname] = [x.strip() for x in nbrstr.split(',')]
    flow[vname] = int(flows)

for v in nbrs:
    for w in nbrs[v]:
        if v < w:
            print(v + str(flow[v]), '<->',w+str(flow[w]),',',end='')
print()

