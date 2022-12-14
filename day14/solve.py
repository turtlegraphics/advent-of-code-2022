#
# Advent of Code 2022
# Bryan Clair
#
# Day 14
#
import sys
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

# import re
# parser = re.compile(r"name:\s*(\w+)\s*val:\s*(\d+)") # or whatever
# name, val = parser.match(line).groups()
# val = int(val)

cave = aocutils.Grid()

source = aocutils.Point(500,0)
# cave[source] = '+'

for line in inputlines:
    tokens = line.split()
    curp = None
    for s in tokens:
        if s == '->':
            continue
        coords = [int(v)for v in s.split(',')]
        corner = aocutils.Point(coords)
        if curp:
            d = (corner - curp).unit()
            d.x = round(d.x)
            d.y = round(d.y) # gross
            p = curp
            cave[p] = '#'
            while p != corner:
                p += d
                cave[p] = '#'
        curp = corner

xmin, ymin, xmax, ymax = cave.bounds()

down = aocutils.Point(0,1)
downL = aocutils.Point(-1,1)
downR = aocutils.Point(1,1)

def drop(cave, source):
    p = source
    moved = True
    while moved and p.y < ymax + 1:
        moved = False
        if (p + down) not in cave:
            p = p + down
            moved = True
        elif (p + downL) not in cave:
            p = p + downL
            moved = True
        elif (p + downR) not in cave:
            p = p + downR
            moved = True
    cave[p] = 'o'
    return True

count = 0
while source not in cave:
    drop(cave,source)
    count += 1

cave.display(vflip=True)
print('part 2:',count)

    
