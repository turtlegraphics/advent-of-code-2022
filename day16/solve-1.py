#
# Advent of Code 2022
# Bryan Clair
#
# Day 16
#
import sys
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

import re
parser = re.compile(r"Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.*)$")

nbrs = {}
flow = {}
open_valves = set()

def pressure(start, timeleft, camefrom=None):
    # returns optimal pressure and the path to do it
    if timeleft == 0:
        return (0,[])

    if timeleft > OUTDEPTH:
        indent = ' '*(30-timeleft)
        print(indent + start)

    # should I open it?
    best = 0
    bestpath = []
    if start not in open_valves and flow[start] > 0:
        # try opening it
        if timeleft > OUTDEPTH:
            print(indent + start + ' opening')
        open_valves.add(start)
        v,path = pressure(start, timeleft - 1)
        v += flow[start]*(timeleft - 1)
        if v > best:
            best = v
            bestpath = ['open'] + path
        open_valves.remove(start)
    for n in nbrs[start]:
        if n != camefrom:
            # try moving to n
            if timeleft > OUTDEPTH:
                print(indent + start + ' moving to ' + n)
            v,path = pressure(n, timeleft - 1, camefrom=start)
            if v > best:
                best = v
                bestpath = [n] + path

    if timeleft > OUTDEPTH:
        print(indent + start + ' found',best,bestpath)
    return (best,bestpath)

for line in inputlines:
    vname, flows, nbrstr = parser.match(line).groups()
    # print(vname, flows, nbrstr)
    nbrs[vname] = [x.strip() for x in nbrstr.split(',')]
    flow[vname] = int(flows)

OUTDEPTH = 27

print(pressure('AA',30))
