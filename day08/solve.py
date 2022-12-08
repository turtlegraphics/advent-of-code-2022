#
# Advent of Code 2022
# Bryan Clair
#
# Day 08
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

forest = aocutils.Grid()
forest.scan(inputlines)

def is_visible(forest,x,y):
    xmin, ymin, xmax, ymax = forest.bounds()
    height = forest[(x,y)]
    # left
    visible = True
    for i in range(xmin, x):
        if forest[(i,y)] >= height:
            visible = False
    if visible:
        return True
    # right
    visible = True
    for i in range(x+1, xmax+1):
        if forest[(i,y)] >= height:
            visible = False
    if visible:
        return True
    # up
    visible = True
    for i in range(ymin, y):
        if forest[(x,i)] >= height:
            visible = False
    if visible:
        return True
    # right
    visible = True
    for i in range(y+1, ymax+1):
        if forest[(x,i)] >= height:
            visible = False
    if visible:
        return True

    return False

def scenic(forest,x,y):
    xmin, ymin, xmax, ymax = forest.bounds()
    height = forest[(x,y)]
    s = 1
    # left
    i = 0
    while x-i > xmin:
        i += 1
        if forest[(x-i,y)] >= height:
            break
    s *= i

    # right
    i = 0
    while x+i < xmax:
        i += 1
        if forest[(x+i,y)] >= height:
            break
    s *= i

    # up
    i = 0
    while y-i > ymin:
        i += 1
        if forest[(x,y-i)] >= height:
            break
    s *= i

    # down
    i = 0
    while y+i < xmax:
        i += 1
        if forest[(x,y+i)] >= height:
            break
    s *= i

    return s

xmin, ymin, xmax, ymax = forest.bounds()
vcount = 0
visgrid = aocutils.Grid()
for x in range(xmin,xmax+1):
    for y in range(ymin, ymax+1):
        vis = is_visible(forest,x,y)
        if vis:
            vcount += 1
        visgrid[(x,y)] = '+' if vis else '.'
#visgrid.display()

print('part 1:',vcount)

best = 0
scenegrid = aocutils.Grid()
for x in range(xmin,xmax+1):
    for y in range(ymin, ymax+1):
        s = scenic(forest,x,y)
        scenegrid[(x,y)] = s
        if s > best:
            best = s
#scenegrid.display()
print('part 2:',best)

    
