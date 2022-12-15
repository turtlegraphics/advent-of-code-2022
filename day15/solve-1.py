#
# Advent of Code 2022
# Bryan Clair
#
# Day 15
#
import sys
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

import re
parser = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")

row = {}

def mark_row(y, s, b):
    dist = s.mandist(b)
    v = abs(s.y - y)
    for dx in range(0, dist-v+1):
        row[s.x + dx] = 1
        row[s.x - dx] = 1

sensors = []
beacons = []
the_row = 2000000

for line in inputlines:
    vals = parser.match(line).groups()
    sx,sy,bx,by = [int(v) for v in vals]
#    print('s',sx,sy,'b',bx,by)
    s = aocutils.Point(sx,sy)
    sensors.append(s)
    b = aocutils.Point(bx,by)
    beacons.append(b)
    mark_row(the_row, s, b)

for b in beacons:
    if b.y == the_row:
        row[b.x] = 0

sum = 0
for k,v in row.items():
    sum += v
print(sum)

    
