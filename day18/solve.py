#
# Advent of Code 2022
# Bryan Clair
#
# Day 18
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

g = {}

dirs = [aocutils.Point3d(x) for x in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]]

minc = [100,100,100]
maxc = [-1,-1,-1]

for line in inputlines:
    p = tuple([int(x) for x in line.split(',')])
    g[p] = '.'
    for i,c in enumerate(p):
        if c < minc[i]:
            minc[i] = c
        if c > maxc[i]:
            maxc[i] = c

size = max(maxc)+1

grid = []
for x in range(size):
    grid.append([])
    for y in range(size):
        grid[x].append(['?']*size)

count = 0
for p in g:
    x,y,z = p
    grid[x][y][z] = '#'
    for d in dirs:
        if tuple(d + aocutils.Point3d(p)) not in g:
            count +=1

print('part 1:',count)

nodes = [(0,0,0)]

def inrange(p):
    if p.x < 0 or p.x >= size:
        return False
    if p.y < 0 or p.y >= size:
        return False
    if p.z < 0 or p.z >= size:
        return False
    return True

while nodes:
    n = nodes.pop()
    p = aocutils.Point3d(n)
    grid[p.x][p.y][p.z] = 'O'
    for d in dirs:
        test = p + d
        if not inrange(test):
            continue
        if grid[test.x][test.y][test.z] == '?':
            t = tuple(test)
            if t not in nodes:
                nodes.append(t)
count = 0
for p in g:
    x,y,z = p
    grid[x][y][z] = '#'
    for d in dirs:
        test = d + aocutils.Point3d(p)
        if not inrange(test):
            count += 1
        elif tuple(test) not in g and grid[test.x][test.y][test.z] == 'O':
            count += 1

print('part 2:',count)
